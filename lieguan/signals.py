import threading

from django.db.models.signals import post_save,post_delete,pre_save,pre_delete
from django.dispatch import receiver
from .models import *
from common.ziptopdf import zip_include_jpg_or_pnp_to_pdf
from common.messagesender import messagesender
from django.core.files import File
from threading import Thread,Timer
from common.middlewares import get_current_user


@receiver(pre_save)
def create_founder(sender, instance, **kwargs):
    if hasattr(instance,'founder'):
        founder=getattr(instance,'founder')
        if not founder:setattr(instance,'founder',get_current_user())

@receiver(pre_save,sender=Personnel)
def for_personnel(sender, instance, **kwargs):
    if instance.num=="":instance.num=None

@receiver(pre_save,sender=Personnel_rc)
def for_personnel_pc(sender, instance, **kwargs):
    if not instance.canceltime and instance.iscancel:instance.canceltime=datetime.datetime.now()

def get_filedict(instance):
    files = {field.name:field.value_from_object(instance) for field in instance._meta.get_fields() if isinstance(field, models.FileField)}
    return files


@receiver(pre_save)
def delete_old_file(sender, instance, **kwargs):
    if sender in [Personnel] :
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
    if sender in [Personnel]:
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
    if sender in [Personnel]:
        obj=sender.objects.get(id=instance.id)
        files = get_filedict(obj)
        for fieldname ,file in files.items():
            if not file:continue
            gx=getattr(obj,fieldname+"_to_pdf")
            if gx and file.path.endswith('.zip'):
                threading.Thread(target=threadz,args=(file,)).start()