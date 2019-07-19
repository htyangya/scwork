from django.db.models.signals import post_save,post_delete,pre_save,pre_delete,m2m_changed
from django.dispatch import receiver
from .models import *
from common.ziptopdf import zip_include_jpg_or_pnp_to_pdf
from common import messagesender
from django.core.files import File
from threading import Thread,Timer
from lieguan.models import Personnel_rc, Personnel
from django.contrib import messages
from common.middlewares import get_current_request

timer_time=2.5
maping={Cost.__name__:Prgsheet,Receipt.__name__:Contract,Equipment_bar.__name__:Equipment}
fieldmaping={Cost.__name__:(['totalcost','money'],)
    ,Receipt.__name__:(['Accepted','money'],)
    ,Equipment_bar.__name__:(["total_number","number"],
                            ["sc_total_number","sc_number"],
                            ["total_money","money"]
    )}

def gettotal(sender, instance, field, ifdelete=False):
    myclass=maping.get(sender.__name__)
    parentname=myclass.__name__.lower()
    parent=getattr(instance,myclass.__name__.lower())
    temp={parentname:parent}
    total=sender.objects.filter(**temp).aggregate(nums=Sum(field))['nums']
    if not total: total = 0
    return  total

@receiver(post_save)
@receiver(post_delete)
def save_models(sender, instance,  **kwargs):  # 保存时生成汇总信息
    if sender.__name__ in maping:
        fieldmaps = fieldmaping.get(sender.__name__)
        myclass = maping.get(sender.__name__)  # 父类类变量，三大单，是sener的外键关联类
        parent = getattr(instance, myclass.__name__.lower())  # 父类实例，instance中的外键
        for fieldmap in fieldmaps:
            parent_total_fieldname = fieldmap[0]
            child_fieldname = fieldmap[1]
            setattr(parent, parent_total_fieldname, gettotal(sender, instance, child_fieldname))
        parent.save()

from common.messagesender import resend_to_jfzj
@receiver(pre_save,sender=Contract)
#和合同保存相关，现包括自动改变收款状态和合同状态两种
def for_contract(sender, instance,  **kwargs):
        if instance.bcfile and not instance.jcfile:
            status="经过补充"
        elif instance.bcfile and instance.jcfile:
            status="补充后已解除"
        elif not instance.bcfile and instance.jcfile:
            status="已解除"
        else:
            status=instance.status
        if instance.status!=status:instance.status=status
        instance.receivable = instance.total_price - instance.Accepted
        if instance.Accepted>0:resend_to_jfzj(instance)
        if instance.total_price > 0:
            #已收结确定之后不能再改变，即使删掉收款单也一样，只有管理员能手动修改。
            if instance.receivable <= 0:
                instance.isfinish = True


@receiver(pre_save)#给进度表/合同生成推送时间和自动办结
def auto_propelling_and_isfinish_for_contract_and_prg(sender, instance,  **kwargs):
    if sender==Prgsheet:
        prg=instance.progress
        #自动生成推送时间，且生成后不再变化
        if instance.ispropelling and not instance.propellingtime:
            instance.propellingtime=datetime.datetime.now()

        if prg and ("办结" in prg or "退单" in prg or "完结" in prg):
            #根据进度自动勾选是否办结
            if not instance.isfinish:
                setattr(instance,"isfinish",True)
    elif sender==Contract:
        if instance.ispropelling and not instance.propellingtime and instance.Accepted>0:
            instance.propellingtime=datetime.datetime.now()


from common.userutil import  encryption_inital_password,accoding_derpartment_match_group
#保存后根据部门名称自动匹配组权限
post_save.connect(accoding_derpartment_match_group,sender=UserProfile)
#保存前调整密码
pre_save.connect(encryption_inital_password,sender=UserProfile)


@receiver(pre_save)#给三大表生成办结时间
def create_finishtime(sender, instance,  **kwargs):
    if sender in [Contract, Prgsheet,Equipment]:
        #自动更新办结、收结时间，且生成后不再改变
        if instance.isfinish==True and not instance.finishtime :
            instance.finishtime=datetime.datetime.now()

def get_filedict(instance):
    files = {field.name:field.value_from_object(instance) for field in instance._meta.get_fields() if isinstance(field, models.FileField)}
    return files

@receiver(pre_save)
def delete_old_file(sender, instance, **kwargs):
    if sender in [Contract,Prgsheet] :
        newfiles=get_filedict(instance)
        oldcontracts=sender.objects.filter(pk=instance.id)
        #如果是第一次创建，之前没有项目，那么不需要删除任何东西
        if oldcontracts:
            oldfiles=get_filedict(oldcontracts[0])
            #如果旧有项目存在，那么根据新上传附件的字段名称查找是否上传过旧有附件
            for fieldname,newfile in newfiles.items():
                oldfile=oldfiles.get(fieldname)
                #如果上传过旧有附件，而且附件名称和新名称不一致，而且本地也存在该附件，那么删除本地附件
                if oldfile and oldfile.name!=newfile.name:
                    if os.path.exists(oldfile.path):os.remove(oldfile.path)

@receiver(post_delete)
def delete_file(sender,instance, **kwargs):
    if sender in [Contract, Prgsheet]:
        files=get_filedict(instance)
        for file in files.values():
            if file and os.path.exists(file.path): os.remove(file.path)


def threadz(file):
    pdf = zip_include_jpg_or_pnp_to_pdf(file.path)
    if pdf:
        file.save("zx.pdf", File(open(pdf, "rb")))
        os.remove(pdf)
        file.instance.save()


@receiver(post_save)
def ziptopdf(sender, instance, created, **kwargs):
    if sender in [Contract, Prgsheet]:
        obj=sender.objects.get(id=instance.id)
        files = get_filedict(obj)
        for fieldname ,file in files.items():
            if not file:continue
            gx=getattr(obj,fieldname+"_to_pdf")
            if gx and file.path.endswith('.zip'):
                threading.Thread(target=threadz,args=(file,)).start()


@receiver(post_save)
def send_notices(sender, instance, created, **kwargs):
    if created and sender in [Prgsheet,Equipment]:
        request=get_current_request()
        code=False
        if sender==Prgsheet:
            per,code=messagesender._messagesender(instance,messagesender.DISPENSE_TO_JFYG)#新建资质合同进度表，发送通知给做单人
        elif sender==Equipment:
             per,code=messagesender._messagesender(instance,messagesender.DISPENSE_TO_LGYG)#新建资质合同配备表，发送通知给配单人
        if code and request: messages.info(request, f"已经成功将该单分发给{instance.owner},请及时提醒对方阅读站内消息")

@receiver(m2m_changed,sender=Equipment_bar.personel.through)
def create_prc(sender, instance, action, reverse, model, pk_set, **kwargs):
    #配备条保存时，检查辖下所有人才是否建立了相同配备条和人才的记录表，如果没有，新建一个。
    if not reverse and action == 'post_add' :
        equipment_bar=instance
        for pid in pk_set:
            # personnel=Personnel.objects.get(id=pid)
            prcs = Personnel_rc.objects.get_or_create(equipment_bar=equipment_bar, personnel_id=pid, contract=equipment_bar.equipment.contract)
    elif not reverse and action == 'post_remove':
        Personnel_rc.objects.filter(equipment_bar=instance,personnel__id__in=pk_set).update(iscancel=True,canceltime=datetime.datetime.now())

