from django.db.models import Q
import contract
from contract.models import *
from notifications.signals import notify
from django.contrib.auth.models import Group
from report.models import zizhireport
from common.middlewares import get_current_user, get_current_request

#target 目标地址
DESC=['有新的资质合同({0})需分配具体做单人',
      '您的上级给您分配了新的业务单({0})，请在两天内上传人员配备信息，并注意更新办理进度',
    '交付部门推送了新进度表({0})给您，请分配具体配单人',
    '您的上级给您分配了新的业务单({0})，请上传配备信息',
    '您的进度表({0})猎管部门已配齐所属人员',
    '有交付已办结单子({0})需要进行回款',
    '({0})已收款完毕，该单收款为{1}元'
       ]

# actor instance 原型
#actor原型          contract          prgsheet        prgsheet        equipment           equipment       prgsheet            contract
TYPESTR=('推送到交付总监', '分发到做单人', '通知猎管配人', '分发到具体配单人', '已配齐通知交付', '通知客服回款', '已收齐通知相关人员')

TYPECHOICE=tuple([(str(index),value) for index,value in enumerate(TYPESTR)])
FLOW_TO_JFZJ=0
DISPENSE_TO_JFYG=1
FLOW_TO_LGZJ=2
DISPENSE_TO_LGYG=3
EP_FINISH_AND_FLOWTO_JF=4
PG_FINISH_AND_FLOWTO_KF=5
CT_FINISH_AND_FLOWTO_CW=6

def _messagesender(instance,type,msg=None,recipient=None):
    # 1、新资质合同(必须是网站生成的)生成，提醒交付总监分配做单人
    #如果进度表已存在，说明是二次推送，那么直接传递进度表给总监
    user=get_current_user(num=False)
    status = "已发送"
    target=instance
    if type==0:
        status = "已发送" if instance.Accepted else"待发送"
        recipient=recipient or Group.objects.get(name='交付总监')
        if Prgsheet.objects.filter(contract_id=instance.id).exists():
            target=instance.prgsheet
    # 2、总监建立新进度表，提醒所属做单人
    elif type==1:
        recipient=recipient or instance.owner

    # 3、做单人点击了推送给猎管,传递具体交付表给猎管总监
    #如果配备记录已存在，说明是二次推送，直接传递配备表给总监
    elif type==2:
        recipient=recipient or  Group.objects.get(name='猎管总监')
        if Equipment.objects.filter(prgsheet_id=instance.id).exists():
            target=instance.euipment

    # 4、猎管总监建立新配备记录，提醒所属配单人，传递配备记录
    elif type==3:
        recipient=recipient or instance.owner
    # 5、猎管人员点击了已配齐（配齐状态由FALSE=>TRUE）,提醒对应进度表的所属人
    #传递进来的instance是一个equipment，但接收人是他的prgsheet,href也必须链接到prg
    elif type==4:
        recipient=recipient or instance.prgsheet.owner
        target = instance.prgsheet
    # 6、交付部门点击了已办结，如果该单未收结，那么通知客服总监进行催款
    elif type==5:
        prjsheet=instance
        target = instance.contract
        recipient = recipient or UserProfile.objects.filter(department='客服总监')
        #如果进度表已办结但合同未收结，并且是有收款单存在的单子，那么才继续
        if not (not prjsheet.contract.isfinish and prjsheet.contract.Accepted and '办结' in prjsheet.progress):
            return False,"办结成功（不需要通知客服的办结单）"
     #7 已收结单子汇报给管理员
    elif type==6:
        recipient=recipient or UserProfile.objects.filter(department='财务中心')
    else:
        return False,"序号超出范围"
    #如果收件人就是自己，那么不进行发送
    if recipient == user and type !=6: return False,"操作成功(通知对象就是自己，无需发送通知)"
    notify.send(sender=instance,
                nfrom=user,
                recipient=recipient,
                status=status,
                type=type,
                verb=TYPESTR[type],
                target=target,
                msg=msg,
                )
    return True,"成功发送通知！"


class BaseChecker:
    def __init__(self) -> None:
        self._respond=False
        self._text=""
    def check(self,*l,**dict):
        pass
    @property
    def respond(self):
        if not self._respond:self.check()
        return self._respond
    @property
    def text(self):
        if not self._text:self.check()
        return self._text

class BaseBtn:
    def __init__(self,text,candialog=True,d_title="",has_msg=False) -> None:
        self.text=text
        self.candialog=candialog
        self.d_title=d_title
        self.has_msg=has_msg
        request=get_current_request()
        request.session[hash(self)]=self


def _check_permisions(instance,type):
    status = instance.get_notify_status(type)
    changepermission = get_current_user(False).has_perm('%s.change_%s' % instance.model_info)
    if type==FLOW_TO_JFZJ:
        return _check_to_jfzj(instance,status,changepermission)
    elif type==DISPENSE_TO_JFYG:
        text=f"确定要分发该单给{instance.owner}吗？确定后系统将给该员工发送消息，" \
            f"您也可以线下进行提醒（注意，总监新建单子时系统已默认自动分发一次，若不是第二次分发，请不要重复操作）。"
    elif type==FLOW_TO_LGZJ:
        text ="该单确定推送给猎管配人吗？点击确定将推送给猎管总监进行任务分发。"
    elif type==DISPENSE_TO_LGYG:
        text=f"确定分发该单给{instance.owner}吗?确定后系统将给该员工发送消息，您也可以线下进行提醒。（注意，总监新建单子时系统已默认自动分发一次，若不是第二次分发，请不要重复操作）"
        return _check_equipment(status, text, changepermission, instance.isfinish)
    elif type==EP_FINISH_AND_FLOWTO_JF:
        text=f"已配齐后会给当前的交付经办人发送消息，您确定给{instance.prgsheet.owner}发送消息吗?"
        return _check_equipment(status,text,changepermission,instance.isfinish)
    elif type==PG_FINISH_AND_FLOWTO_KF:
        text="点击确定将会手动办结此进度表,办结后进度表处于锁定状态不可再编辑！若该单有尾款,还会自动给客服部门推送消息。"
    elif type==CT_FINISH_AND_FLOWTO_CW:
        text="点击确定将会手动收结此合同,收结后合同处于锁定状态不可再编辑，请核实无余款后点击确认！"
    return _general_check(status,text,changepermission,instance.isfinish)

def _general_check(status,text,changepermission,isfinish):
    if isfinish:text="该表已办结/收结，处于锁定状态，不可再进行操作！"
    elif not changepermission:text="您没有权限操作此表!"
    elif status!="全部已读":text="上一条推送消息对方还未读，必须已读之后才能推送下一条消息！"
    return status=="全部已读" and not isfinish and changepermission,text

def _check_equipment(status,text,changepermission,isfinish):
    if not changepermission:
        text = "您没有权限操作此表!"
    elif status != "全部已读":
        text = "上一条推送消息对方还未读，必须已读之后才能推送下一条消息！"
    return status == "全部已读" and changepermission, text

def _check_to_jfzj(contract,notify_status,changepermission):

    if contract.Accepted:
        text = "确定推送给消化部门进行办理吗?该单已收款，确认发送将直接发送消息给消化人员。"
    else:
        text="确定推送给消化部门进行办理吗?该单未收款，确认发送后将发送一条待发送的消息，等财务人员收首笔款后系统将自动发送该消息。"
    per,code=_general_check(notify_status,text,changepermission,contract.isfinish)
    if per==False:return per,code
    if notify_status == "等待发送":
        text = "您已经发送了一条推送消息，因为该单还未收款，所以处于待发送状态，请等待信息发送并且对方阅读后再继续推送。"
    elif notify_status == "等待已读":
        text = "上一条推送消息对方还未读，必须已读之后才能推送下一条消息！"
    return per,text

def submit_done(instance,type,msg):
    per,code=_check_permisions(instance,type)
    if not per:return per,code
    if type in (0,2):
        instance.ispropelling=True
        instance.save()
    elif type in (4,5,6):
        instance.isfinish=True
        if type==4:instance.set_finishtime_recorde()
        instance.save()
    return _messagesender(instance,type,msg)

def resend_to_jfzj(contract):
    notify_status = contract.get_notify_status(type=0)
    if notify_status=="等待发送" and contract.Accepted:
        contract.notifies.filter(status='待发送').update(status='已发送',timestamp=datetime.datetime.now())

