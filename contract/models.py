import datetime
import json
import os

import django,datetime,threading,functools
from django.contrib.contenttypes.fields import GenericRelation
from common.middlewares import get_current_user
from scwork.settings import MEDIA_ROOT
from django.db import models
from django.utils.safestring import mark_safe
from django.db.models import Sum
from custom.models import Custom
from django.contrib.auth.models import User
from users.models import UserProfile
from common.basemodel import Basemodel,model_meta_register
import jsonfield

def set_file_path(instance, filename,modelname,typename):
    num = str(instance)
    year = datetime.date.today().year
    moon = datetime.date.today().month
    type = typename + os.path.splitext(filename)[-1]
    return f'{modelname}/{year}/{moon}/{num}_{type}'


def prgsheet_path(instance, filename,name):
    num=str(instance)
    year=datetime.date.today().year
    moon=datetime.date.today().month
    name=name+os.path.splitext(filename)[-1]
    return 'prgsheet/{0}/{1}/{2}_{3}'.format(year,moon,num, name)
def contract_path(instance,filename,name):
    year = datetime.date.today().year
    moon = datetime.date.today().month
    name = name + os.path.splitext(filename)[-1]
    return 'contract/{0}/{1}/{2}_{3}'.format(year,moon,instance.num,name)


@model_meta_register
class Contract(Basemodel):
    CON_TYPE=(
        ("资质合同", "资质合同"),
        ("工商","工商"),
        ("工商注销", "工商注销"),
        ("食品经营", "食品经营"),
        ("条形码", "条形码"),
        ("财务记账", "财务记账"),
        ("人力资源", "人力资源"),
        ("认证服务", "认证服务"),
        ("网站开发", "网站开发"),
        ("人力资源", "人力资源"),
        ("商标", "商标"),
        ("委托协议", "委托协议"),
        ("培训协议", "培训协议"),
        ("LOGO设计", "LOGO设计"),
        ("人才协议", "人才协议"),
        ("专利合同", "专利合同"),
        ("企业咨询", "企业咨询"),
        ("著作权", "著作权"),
        ("专利合同", "专利合同"),
        ("劳务派遣", "劳务派遣"),
        ("其他合同", "其他合同"),
    )
    STATUS = (("正常状态", "正常状态"), ("补充后已解除", "补充后已解除"), ("经过补充", "经过补充"), ("已解除", "已解除"))

    list_display = ['get_option_html','name','custom','singman','signdate','year','total_price','contract_type','status','Accepted','receivable','isfinish','ispropelling','get_file','createtime','propellingtime','finishtime']
    readonly_fields = ['ispropelling','isfinish','propellingtime','name', 'Accepted', 'receivable', 'createtime', 'updatetime', 'finishtime','founder']
    search_fields=['id','num', 'name', 'custom__name']

    custom=models.ForeignKey(Custom,on_delete=models.CASCADE,verbose_name='客户名称')
    name=models.CharField("合同名称", max_length=200, blank=True)
    num=models.CharField("合同编号",max_length=200,unique=True,help_text="注意，该编号不能重复")
    singman=models.CharField("签单人",max_length=200,blank=True)
    signdate=models.DateField("签单日期",default=datetime.date.today)
    year=models.CharField("年度",max_length=4,default=datetime.date.today().year)
    total_price=models.FloatField("合同金额（元）")
    contract_type=models.CharField("合同分类",max_length=200,choices=CON_TYPE,default="资质合同")

    comment=models.TextField("合同备注",blank=True,help_text="合同注意事项可以填写此处")
    update_by = models.CharField("数据生成方式", max_length=200,choices=(('管理员脚本上传',"管理员脚本上传"),('网站生成',"网站生成")),default='网站生成')
    file=models.FileField("合同附件", upload_to=functools.partial(set_file_path,modelname="contract",typename="合同附件"),null=True, blank=True,
                          help_text = '勾选转化为PDF，会将默认将上传的zip压缩包转化为pdf，请确认压缩包格式为zip，并且压缩包中的图片格式为pnp或jpg')
    file_to_pdf=models.BooleanField("转化为PDF", default=True)
    status=models.CharField("合同状态",max_length=10,default='正常状态',choices=STATUS)
    founder = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.PROTECT,default=get_current_user
                                )
    #补充合同附件
    bcfile = models.FileField("补充合同附件", upload_to=functools.partial(set_file_path,modelname="contract",typename="补充合同附件"), null=True, blank=True,)
    bcfile_to_pdf = models.BooleanField("转化为PDF", default=True)
    #解除合同附件
    jcfile = models.FileField("解除/终止合同附件", upload_to=functools.partial(set_file_path,modelname="contract",typename="解除合同附件"), null=True, blank=True, )
    jcfile_to_pdf = models.BooleanField("转化为PDF", default=True)

    #以下资质类常用
    itemcontent=models.TextField("项目具体内容",blank=True)
    payment=models.TextField("付款方式",blank=True)
    deadline=models.IntegerField("合同期限（工作日）",blank=True,null=True,help_text="填写该合同最长的期限时间，以工作日为单位，详细描述填写到下一个字段")
    deadline_text = models.CharField("合同期限详细描述", max_length=200, blank=True,help_text="填写期限描述，例如分阶段的期限")
    deadline_date=models.DateField("预计合同截止日期",null=True,blank=True,help_text='请根据合同期限填写截止日期，所有超期未办结的资质类单子将在首页进行提醒')
    ispropelling = models.BooleanField("通知消化部门", default=False)
    propellingtime = models.DateTimeField("通知消化时间", blank=True, null=True)
    #自动生成
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    updatetime = models.DateTimeField("修改时间", auto_now=True)
    finishtime=models.DateTimeField("收结时间", null=True,blank=True)
    #收款单相关
    Accepted = models.FloatField("收款单.已收", default=0)
    receivable = models.FloatField("收款单.未收", default=0)
    isfinish=models.BooleanField("是否收结",default=False)
    #gr泛类型反向映射
    notifies=GenericRelation('notifications.Notification',
                             object_id_field='actor_object_id',content_type_field='actor_content_type',
                             related_query_name='contract'
                             )

    def __str__(self):
        return self.name

    def get_file(self):
        re=''
        if self.file:
            re= f'<a href="/media/{self.file}" target="_blank"><span class="badge" style="background-color:#1b9dec;color:white">合同</span></a>'
        if self.bcfile:
            re=re+f'<a href="/media/{self.bcfile}" target="_blank"><span class="badge" style="background-color: green;color:white">补充</span></a>'
        if self.jcfile:
            re = re + f'<a href="/media/{self.jcfile}" target="_blank"><span class="badge" style="background-color: blue;color:#white">解除</span></a>'
        if re:return mark_safe(re)
        return "空"
    get_file.short_description="附件"

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = verbose_name
        permissions = (
            ("viewall_contract", "Can 查看所有合同"),
            ("viewcompany_contract", "Can 查看分公司所有合同"),
            ("vewowner_contract", "Can 查看个人合同"),
            ("export_contract", "Can 导出合同"),
        )

@model_meta_register
class Receipt(Basemodel):
    list_display = ['get_option_html','contract', 'pay_type','pay_by', 'pay_dep', 'money', 'pay_description', 'pay_info',
                     'received_acount','received_time','createtime','founder',]
    readonly_fields = ['createtime','founder']
    search_fields = ['contract__num', 'contract__name','id']
    def __str__(self):
        return "SKD-"+ str(self.id)
    STYLE=(
        ("现金","现金"),
        ("银行转账","银行转账"),
        ("电子支付","电子支付"),
        ("其他","其他"),
    )
    RECEIVED_ACOUNT=(('贵州银行','贵州银行'),('贵州银行8243','贵州银行8243'),('贵州银行510','贵州银行510'),
                     ('工商银行624','工商银行624'),('建设银行','建设银行'),('农业银行2174','农业银行2174'),('信用合作社','信用合作社'),('富明村镇银行','富明村镇银行'),
                     ('首途知产对公','首途知产对公'),('首辰财务对公','首辰财务对公'),('电子支付','电子支付'),('现金','现金'),)
    contract=models.ForeignKey(Contract,on_delete=models.CASCADE,verbose_name="合同")
    pay_type=models.CharField("收款/退款",max_length=10,choices=(('收款','收款'),('退款','退款')),default="收款")
    pay_by=models.CharField("收款方式",max_length=10,choices=STYLE,default="银行转账")
    pay_dep=models.CharField("银行帐号/机构名称",max_length=50,help_text="请填写对方打款具体银行及汇款帐号，电子支付填写微信/支付宝等应用名称",blank=True)
    pay_info=models.CharField("汇款信息",max_length=200,help_text="如有必要,可填写对方汇款信息,包括对方姓名、身份证号等",blank=True)
    money=models.FloatField("收款金额(元)")
    received_acount=models.CharField("收款帐号",max_length=50,choices=RECEIVED_ACOUNT,default='贵州银行')
    pay_description = models.CharField("收款描述", max_length=200, help_text="请填写收款信息，比如首笔款、进度款等")
    received_time=models.DateTimeField("实际收款时间",default=django.utils.timezone.now)
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    founder = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.PROTECT,default=get_current_user
                                )


    class Meta:
        verbose_name = '财务：收款单'
        verbose_name_plural = verbose_name
        permissions = (
            ("viewall_receipt", "Can 查看所有收款单"),
            ("viewcompany_receipt", "Can 查看分公司所有收款单"),
            ("vewowner_receipt", "Can 查看个人收款单"),
            ("export_receipt", "Can 导出收款单"),
        )

@model_meta_register
class Prgsheet(Basemodel):
    list_display = ['get_option_html','owner', 'contract', 'get_city', 'ownerrecord', 'approval_dep', 'approval_address', 'type',
                    'progress',  'isfinish', 'totalcost', 'get_file', 'createtime','propellingtime', 'finishtime']
    readonly_fields = ['ispropelling','isfinish','createtime', 'updatetime', 'totalcost', 'finishtime','propellingtime']
    search_fields = ['contract__num', 'contract__name','id']

    contract=models.OneToOneField(Contract,on_delete=models.CASCADE,verbose_name="合同")
    ownerrecord=models.CharField("做单人记录",max_length=200,help_text="做单人存在更换情况在此记录",blank=True)
    owner=models.ForeignKey(UserProfile, verbose_name="当前做单人", on_delete=models.PROTECT)
    approval_dep = models.CharField("审批部门", max_length=200,blank=True)
    approval_address=models.CharField("审批部门地址",max_length=200,blank=True)
    type = models.CharField("资质类别", max_length=200,help_text="资质申请业务（新办/增项/升级）",blank=True)
    progress=models.CharField("办理进度",max_length=200,help_text="未启动/已启动/差安证/差增项/已退单/已办结等",blank=True,null=True,default=None)
    prg_explain=models.TextField("进度说明",blank=True)
    isfinish=models.BooleanField("是否办结",default=False)
    ispropelling = models.BooleanField("是否通知猎管配人", default=False)
    file = models.FileField("相关附件", upload_to=functools.partial(set_file_path,modelname="prgsheet",typename="进度表附件"), null=True, blank=True,
                            help_text='勾选转化为PDF，会将默认将上传的zip压缩包转化为pdf，请确认压缩包格式为zip，并且压缩包中的图片格式为pnp或jpg')
    file_to_pdf = models.BooleanField("转化为PDF", default=True)
    #以下是人员配备内容
    jianzaoshi=models.TextField("建造师",help_text="注明：级别、专业、人数",blank=True)
    jsfzr=models.TextField("技术负责人",help_text="注明：职称级别、专业、工程管理经历年限、人数",blank=True)
    gongchengshi=models.TextField("工程师",help_text="注明：专业、人数",blank=True)
    # xcglry=models.TextField("现场管理人员",help_text="注明：专业、人数",blank=True)
    jigong=models.TextField("技工",help_text="注明：级别、工种、人数",blank=True)
    tezhonggong=models.TextField("特种工",help_text="注明：级别、工种、人数",blank=True)
    sanleirenyuan=models.TextField("三类人员",help_text="注明：级别",blank=True)
    ohter=models.TextField("其他",help_text="其他人员",blank=True)
    totalcost=models.FloatField("成本汇总", default=0)
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    updatetime = models.DateTimeField("修改时间", auto_now=True)
    propellingtime = models.DateTimeField("通知猎管时间", blank=True,null=True)
    finishtime = models.DateTimeField("办结时间", null=True, blank=True)
    # gr泛类型反向映射
    notifies = GenericRelation('notifications.Notification',
                               object_id_field='actor_object_id', content_type_field='actor_content_type',
                               related_query_name='prgsheet'
                               )
    def __str__(self):
        return "JDB-"+str(self.id)

    def get_file(self):
        if self.file:
            return mark_safe(f'<a href="/media/{self.file}" target="_blank"><span class="badge" style="background-color:#1b9dec;color:white">附件</span></a>')

        return "空"
    get_file.short_description="附件"
    def get_city(self):
        return self.contract.custom.city
    get_city.short_description="城市"

    class Meta:
        verbose_name = '交付：进度表'
        verbose_name_plural = verbose_name
        permissions = (
            ("viewall_prgsheet", "Can 查看所有进度表"),
            ("viewcompany_prgsheet", "Can 查看分公司所有进度表"),
            ("vewowner_prgsheet", "Can 查看个人进度表"),
            ("export_prgsheet", "Can 导出进度表"),
        )

@model_meta_register
class Cost(Basemodel):
    list_display = ['get_option_html','prgsheet', 'type', 'forwhat', 'money', 'createtime','founder']
    readonly_fields = ['createtime','founder']
    prgsheet=models.ForeignKey(Prgsheet,on_delete=models.CASCADE,verbose_name="进度表")
    type = models.CharField("费用类型", max_length=200,help_text="培训费/公关费等")
    forwhat=models.CharField("费用事由", max_length=200,help_text="用于什么公司的什么费用")
    money = models.FloatField(" 费用金额(元)")
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    founder = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.PROTECT, null=True, blank=True,
                                default=get_current_user)
    def __str__(self):
        return "CBD-" + str(self.id)
    class Meta:
        verbose_name = '成本单'
        verbose_name_plural = verbose_name

@model_meta_register
class Equipment(Basemodel):
    list_display = ['get_option_html','owner', 'get_barlist', 'prgsheet', 'contract', 'total_number', 'sc_total_number', 'total_money',
                    'isfinish', 'createtime','finishtime']
    readonly_fields = ['isfinish', 'contract','total_number', 'sc_total_number', 'total_money', 'createtime', 'updatetime',
                       'finishtime','finishtime_recorde']
    search_fields = ['contract__num', 'contract__name', 'id']

    prgsheet=models.OneToOneField(Prgsheet,on_delete=models.CASCADE, verbose_name="进度表")
    owner = models.ForeignKey(UserProfile, verbose_name="配备人", on_delete=models.PROTECT)
    isfinish = models.BooleanField("是否配齐", default=False)
    comment = models.TextField("备注说明", blank=True, help_text="工作进度和特殊说明应填写此处")
    total_number=models.IntegerField("总人数", default=0)
    sc_total_number=models.IntegerField("首涂需提供总人数", default=0)
    total_money=models.FloatField("总费用", default=0)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name="合同")
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    updatetime = models.DateTimeField("修改时间", auto_now=True)
    finishtime = models.DateTimeField("最初配齐时间", null=True, blank=True)
    finishtime_recorde=jsonfield.JSONField("配齐时间记录",max_length=1000)
    # gr泛类型反向映射
    notifies = GenericRelation('notifications.Notification',
                               object_id_field='actor_object_id', content_type_field='actor_content_type',
                               related_query_name='euipment'
                               )

    def get_barlist(self):
        id=self.id
        links=f'<a href="/contract/equipment_bar/?_rel_equipment__id__exact={id}"><span class="badge" style="background-color:#1b9dec;color:white">金额</span></a></a> <br/>'
        links=links+f'<a href=/lieguan/personnel/?_p_equipment_bar__equipment__prgsheet__contract__id__exact={self.contract.id}><span class="badge" style="background-color:#1b9dec;color:white">人才</span></a> <br/>'
        links=links+f'<a href=/lieguan/personnel_rc/?_p_contract__id__exact={self.contract.id}><span class="badge" style="background-color:#1b9dec;color:white">人才使用</span></a>'
        return  mark_safe(links)
    get_barlist.short_description="明细表"

    def set_finishtime_recorde(self):
        dict=self.finishtime_recorde
        length = len(dict) + 1
        dict[f"第{length}次配齐"]=datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
        self.finishtime_recorde=dict

    def __str__(self):
        return "PBJL-" +str(self.id)
    class Meta:
        verbose_name = '猎管：配备记录'
        verbose_name_plural = verbose_name
        permissions = (
            ("viewall_equipment", "Can 查看所有配备记录"),
            ("viewcompany_equipment", "Can 查看分公司所有配备记录"),
            ("vewowner_equipment", "Can 查看个人配备记录"),
            ("export_equipment", "Can 导出配备记录"),
        )

class Subject(models.Model):
    name=models.CharField("专业/工种", max_length=200,unique=True)
    class Meta:
        verbose_name = '专业/工种'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Equipment_bar(models.Model):
    MAJORTYPE=['建造师','技术负责人','工程师','现场管理人员','技工','特种工','三类人员','其他注册类人员','其他']
    MJ_TUPPLE=tuple([(each,each)for each in MAJORTYPE])
    LEVEL=['初级','中级','高级','一级','二级','三级','A','B','C']
    LV_TUPPLE=tuple([(each,each)for each in LEVEL])
    equipment=models.ForeignKey(Equipment,on_delete=models.CASCADE, verbose_name="配备记录")
    major_type=models.CharField("所属大类", max_length=200, choices=MJ_TUPPLE)
    subject_or_worktype=models.ForeignKey(Subject,on_delete=models.PROTECT,verbose_name="工种/专业",blank=True,null=True,
                                          help_text="如果没有您想要的专业/工种请点击右边的+添加")
    level=models.CharField("级别/证书级别", max_length=200, choices=LV_TUPPLE,blank=True)
    ohter=models.CharField("年限或其他描述", max_length=200,blank=True)
    number = models.IntegerField("总人数", default=0)
    sc_number = models.IntegerField("首涂需提供人数", default=0)
    money = models.FloatField("费用", default=0)
    specific=models.CharField("其他非系统人员", max_length=300,blank=True)
    personel=models.ManyToManyField('lieguan.Personnel',verbose_name="系统人才库",blank=True)
    comment=models.CharField("备注说明", max_length=200,blank=True)

    def __str__(self):
        return "PBT-" +str(self.id)
    class Meta:
        ordering=["-id"]
        verbose_name = '配备条'
        verbose_name_plural = verbose_name




