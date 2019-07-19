from django.http import HttpResponse
from contract.models import *
from users.models import UserProfile
from django.contrib.auth.models import Group
import json
from xadmin.models import Bookmark,UserSettings,UserWidget

jiaofu='{"title": "交付总监待办：新资质合同需匹配进度表", "bookmark": "2"}'
kefu='{"title": "客服总监待办：已办结资质单未收结需回款", "bookmark": "3"}'
lieguan='{"title": "猎管总监待办：有进度表需新建配备记录", "bookmark": "1"}'
bookmarks_to_all=[jiaofu,lieguan,kefu]
us_key='dashboard:home:pos'

def encryption_inital_password(sender, instance,  **kwargs):
    user=instance
    if user.password=="zxcvbnm,1":user.set_password(user.password)


def accoding_derpartment_match_group(sender, instance, created, **kwargs):
    user=instance
    if not user.groups.filter(name="仅查看组").exists():user.groups.add(Group.objects.get(name='仅查看组'))
    add_group=[]
    if user.department:
        for group in Group.objects.all():
            if group.name in user.department and not user.groups.filter(id=group.id).exists():
                add_group.append(group)
    if add_group:user.groups.add(*add_group)

def update_userwidget_from_bta(user):
    for bm in bookmarks_to_all:
        #查看当前user是否存在列表中的书签组件
        uw=UserWidget.objects.filter(user_id=user.id,value__contains=bm)
        if not uw:
            #不存在就新建一个
            UserWidget.objects.create(page_id='home',widget_type='书签',value=bm,user=user)

def update_usersettings(user):
    uw=UserWidget.objects.filter(user=user).values_list('id',flat=True)
    us=UserSettings.objects.filter(user=user)
    if uw:
        uw = [str(tem) for tem in uw]
        if us:
            instance=us.first()
            instance.value=",".join(uw)
            instance.save()
        else:
            UserSettings.objects.create(key=us_key,user=user,value=",".join(uw))







