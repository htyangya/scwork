import datetime
import functools
import os
from django.db import models
from django.utils.safestring import mark_safe
from users.models import UserProfile, Company
from contract.models import Equipment_bar, Subject, Contract
from django.db.models import F, Max, Q,Count
from common.middlewares import get_current_user,get_current_company
from common.basemodel import Basemodel as Base_model,model_meta_register
from common import utils
def set_file_path(instance, filename, modelname, typename):
    num = str(instance)
    year = datetime.date.today().year
    moon = datetime.date.today().month
    type = typename + os.path.splitext(filename)[-1]
    return f'{modelname}/{year}/{moon}/{num}_{type}'

class Basemodel(Base_model):
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    updatetime = models.DateTimeField("修改时间", auto_now=True)
    founder = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.PROTECT, null=True, blank=True,
                                default=get_current_user)
    class Meta:
        abstract = True

def _nextyeardate():
    return datetime.date.today() + datetime.timedelta(days=365)

@model_meta_register
class Personnel(Basemodel):
    list_display = ['get_option_html', 'name', 'gender', 'contact_man', 'tel', 'major_type', 'subject_or_worktype',
                    'level', 'money', 'islive','canreuse', 'singman', 'get_file', 'get_status', 'signdate', 'enddate',
                    'founder']
    readonly_fields = ['createtime', 'updatetime', 'founder','company']
    search_fields = ['name', 'num','equipment_bar__equipment__prgsheet__contract__name']
    GENDER = (("男", "男"), ("女", "女"),)
    name = models.CharField("姓名", max_length=10)
    num = models.CharField("身份证号", max_length=50, null=True, blank=True)
    gender = models.CharField("性别", max_length=1, choices=GENDER)
    contact_man = models.CharField("联系人", max_length=200, blank=True)
    tel = models.CharField("电话号码", max_length=50, blank=True)
    major_type = models.CharField("所属大类", max_length=200, choices=Equipment_bar.MJ_TUPPLE)
    subject_or_worktype = models.ManyToManyField(Subject, verbose_name="工种/专业",
                                                 help_text="如果没有您想要的专业/工种请点击右边的+添加")
    level = models.CharField("级别/证书级别", max_length=200, choices=Equipment_bar.LV_TUPPLE, blank=True)
    money = models.FloatField("金额（元）")
    singman = models.CharField("签单人", max_length=200, blank=True)
    signdate = models.DateField("合同签订日期", default=datetime.date.today)
    enddate = models.DateField("合同到期日期", default=_nextyeardate)
    islive = models.BooleanField('当前可用', default=True)
    canreuse = models.BooleanField('可否重复利用', default=True,help_text="筛选选取时，默认选取可重用中已办结的，和不可重用中未被使用的（建造师默认可重用）")
    comment = models.TextField("备注", blank=True)
    file = models.FileField("合同附件", upload_to=functools.partial(set_file_path, modelname="personnel", typename="合同附件"),
                            null=True, blank=True,
                            help_text='勾选转化为PDF，会将默认将上传的zip压缩包转化为pdf，请确认压缩包格式为zip，并且压缩包中的图片格式为pnp或jpg')
    file_to_pdf = models.BooleanField("转化为PDF", default=True)
    zsfile = models.FileField("证书等其他附件", upload_to=functools.partial(set_file_path, modelname="personnel", typename="证书等其他附件"),
                            null=True, blank=True)
    zsfile_to_pdf = models.BooleanField("转化为PDF", default=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="所属分公司", default=get_current_company)

    def __str__(self):
        return self.name
    def _from_this_get_statushtml(self,name,isfinish):
        if not name:return "空"
        span='<span class="badge" style="background-color:grey;color:white">未</span>'if not isfinish else '<span class="badge" style="background-color:#1b9dec;color:white">结</span>'
        return mark_safe(f'<p class="text-muted"> '
                         +span+
                        f'<small>{name}</small>'
                        f'</p> '
                         )

    def get_status(self):
        eb=self.equipment_bar_set.all().first()
        if not eb :return "空"
        prgsheet= eb.equipment.prgsheet
        prg_isfinish=prgsheet.isfinish
        value=prgsheet.contract.name
        name=prgsheet.contract.get_model_link('list')
        return self._from_this_get_statushtml(name, prg_isfinish)
    get_status.short_description = "当前使用"

    @staticmethod
    def filter(major_type, level=None, subject_name=None,id_list=None,type="normal", **dict):

        filter_dict = {}
        filter_dict["islive"] = True
        if major_type:filter_dict["major_type"] = major_type
        if level: filter_dict["level"] = level
        if subject_name: filter_dict["subject_or_worktype__name"] = subject_name
        if dict: filter_dict.update(dict)

        if major_type == "建造师":
            # 建造师，只能搜索到没有被使用过，或者上一次使用记录已经办结的人才`
            condition=(Q(equipment_bar__id=F
            ('maxid')) & Q(equipment_bar__equipment__prgsheet__isfinish=True) | Q(maxid__isnull=True))

        else:    # 如果不是建造师，能搜索到可重用中的已办结，以及不可重用中的未使用过人才
            condition=(Q(canreuse=False)&Q(equipment_bar__isnull=True))|(Q(canreuse=True)&(Q(maxid__isnull=True)|(Q(equipment_bar__id=F('maxid')) & Q(equipment_bar__equipment__prgsheet__isfinish=True))))
        if id_list:condition=(condition|Q(id__in=id_list))
        if type=="only_multi":
            condition=(condition)&Q(s_count__gt=1)
        qs = Personnel.objects.all().annotate(maxid=Max("equipment_bar__id"),s_count=Count("subject_or_worktype")).filter(**filter_dict)
        qs1= qs.filter(condition).order_by("-s_count","-updatetime")
        if type=="reverse":qs1= qs.exclude(id__in=qs1)

        return qs1.distinct().prefetch_related('equipment_bar_set__equipment__prgsheet__contract','subject_or_worktype')


    def get_file(self):
        user=get_current_user()
        info=user.has_perm('%s.info_%s' % self.model_info)
        re=''
        if self.zsfile:
            re = f'<a href="/media/{self.zsfile}" target="_blank"><span class="badge" style="background-color:#1b9dec;color:white">证书</span></a>'
        if self.file and info:
            re=re+f'<a href="/media/{self.file}" target="_blank"><span class="badge" style="background-color:#1b9dec;color:white">合同</span></a>'
        if re:
            return mark_safe(re)
        return "空"
    get_file.short_description = "附件"

    class Meta:
        ordering=['updatetime']
        verbose_name = '猎聘人才'
        verbose_name_plural = verbose_name
        unique_together=['name','major_type']
        permissions = (
            ("viewall_personnel", "Can 查看所有猎管人才"),
            ("viewcompany_personnel", "Can 查看分公司所有猎管人才"),
            ("vewowner_personnel", "Can 查看个人猎管人才"),
            ("export_personnel", "Can 导出猎管人才"),
            ("info_personnel", "Can 查看人才所有信息"),
        )

@model_meta_register
class Personnel_rc(Basemodel):
    # 人才的使用记录，主要是人才外键，合同外键，为了能和配备条联动，保存一个配备条外键
    # 当配备条保存时，自动为每一个人才personnel保存一个prc，存储personnel（f）、contract（f）、equipment（f）三个
    list_display = ['personnel', 'contract', 'createtime', 'founder','iscancel','canceltime']
    search_fields = ['personnel__name', 'contract__num']
    readonly_fields = ['personnel', 'contract', 'createtime', 'founder', 'equipment_bar', 'updatetime','canceltime']
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, verbose_name='人才')
    equipment_bar = models.ForeignKey(Equipment_bar, on_delete=models.CASCADE, verbose_name='配备条')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='合同')
    iscancel = models.BooleanField('是否已从该公司调出', default=False)
    canceltime = models.DateTimeField("调出时间", blank=True,null=True)
    def __str__(self):
        return "RCJL-" + str(self.id)

    class Meta:
        verbose_name = '人才使用记录'
        verbose_name_plural = verbose_name
        permissions = (
            ("viewall_personnel_rc", "Can 查看所有人才使用记录"),
            ("viewcompany_personnel_rc", "Can 查看分公司所有人才使用记录"),
            ("vewowner_personnel_rc", "Can 查看个人人才使用记录"),
            ("export_personnel_rc", "Can 导出人才使用记录"),
        )