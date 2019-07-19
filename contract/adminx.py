from django.contrib.auth import get_permission_codename
from django.urls import reverse
from common.messagesender import submit_done, _check_permisions as get_tupple
from common import messagesender
from xadmin.layout import Fieldset, Row
from common.basemodel import Baseadminmodel,adminx_register
import xadmin, time
from .resources import *

@adminx_register
class Contractmodel(Baseadminmodel):
    mymodel = Contract
    required_fields = ['deadline', 'deadline_date']
    required_update_or_add = "add"
    list_filter = mymodel.get_fields() + Custom.get_fields(True) + Prgsheet.get_fields(True) + Equipment.get_fields(
        True)
    ordering = ['-updatetime']
    model_icon = 'fa fa-book'
    list_bookmarks = [{
        "title": "合同截止日期提醒",
        "query": {"deadline_date__lt": (datetime.date.today() + datetime.timedelta(days=60)),
                  'contract_type__exact': '资质合同',
                  'prgsheet__isfinish__exact': 0

                  }
    }]
    form_layout = (
        Fieldset((u'通用'),
                 'custom', "num",
                 Row('name', 'status'),
                 'singman', 'signdate', 'year',
                 'total_price', 'contract_type', Row('file', 'file_to_pdf'),
                 'update_by', 'comment', 'founder',
                 Row('createtime', 'updatetime', 'finishtime', 'propellingtime'),
                 css_class='unsort'),
        Fieldset('解除或补充合同',
                 Row('bcfile', 'bcfile_to_pdf'),
                 Row('jcfile', 'jcfile_to_pdf'),
                 css_class='unsort',
                 ),

        Fieldset('收款单自动汇总',
                 Row('Accepted', 'receivable'),
                 'isfinish',
                 css_class='unsort',
                 ),
        Fieldset('资质合同专项',
                 Row('deadline', 'deadline_date'),
                 Row('deadline_text', 'ispropelling'),
                 'itemcontent',
                 'payment',
                 css_class='unsort'),
    )

    def get_btns(self):
        bnt1_per, bnt1_text = get_tupple(self.obj, messagesender.CT_FINISH_AND_FLOWTO_CW)
        bnt2_per, bnt2_text = get_tupple(self.obj, messagesender.FLOW_TO_JFZJ)

        btns = [
            {'text': '点击已收结',
             'candialog': True,
             'd_title': '手动更新收结状态',
             'd_hasper': bnt1_per,
             'd_text': bnt1_text,
             'd_url': self.get_submit_url(messagesender.CT_FINISH_AND_FLOWTO_CW),
             'has_msg': False,
             },
            {'text': '推送给消化',
             'candialog': True,
             'd_title': '推送给消化进行办理',
             'd_hasper': bnt2_per,
             'd_text': bnt2_text,
             'd_url': self.get_submit_url(messagesender.FLOW_TO_JFZJ),
             'has_msg': True,
             },
            {'text': '返回列表页',
             'candialog': False,
             'd_url': self.obj.get_model_url('list'),
             },
        ]
        return btns

    # def has_change_permission(self, obj=None):
    #     perm = super().has_change_permission(obj)
    #     if obj:
    #         perm = self.user.is_superuser or (perm and not obj.isfinish)
    #     return perm

    def save_models(self):  # 保存时生成合同名称
        obj = self.new_obj
        custom_name = obj.custom.name
        contract_name = custom_name + obj.contract_type + obj.num
        if obj.name != contract_name: obj.name = contract_name
        obj.save()

    def get_form_datas(self):
        params = super(Contractmodel, self).get_form_datas()
        if not self.org_obj and self.request.method != 'POST':
            year = time.strftime('%y')
            params['initial']['num'] = f"G{year}-"
        return params

@adminx_register
class Receiptmodel(Baseadminmodel):
    mymodel = Receipt
    list_filter = mymodel.get_fields() + Contract.get_fields(True)
    aggregate_fields = {"money": "sum"}
    model_icon = 'fa fa-money'

@adminx_register
class Prgsheetmoel(Baseadminmodel):
    list_select_related = ['owner', 'contract', 'contract__custom']
    import_export_args = {'import_resource_class': Prg_im_resource, 'export_resource_class': Prg_ex_resource}
    mymodel = Prgsheet
    list_filter = mymodel.get_fields() + Contract.get_fields(True) + Equipment.get_fields(True)
    model_icon = 'fa fa-circle'
    ordering = ['-updatetime']
    required_fields = ['progress', 'approval_dep', 'approval_address', 'type', 'prg_explain',
                       'jianzaoshi', 'jsfzr', 'gongchengshi', 'jigong', 'sanleirenyuan', 'tezhonggong', 'ohter', ]
    form_layout = (
        Fieldset((u'进度表'),
                 'contract', Row('ownerrecord', 'owner'), Row('approval_dep', 'approval_address'),
                 Row('type', 'progress', ), 'totalcost', Row('file', 'file_to_pdf'),
                 'prg_explain', Row('createtime', 'updatetime', 'finishtime', 'propellingtime'),
                 Row('isfinish', 'ispropelling'),
                 css_class='unsort'),
        Fieldset('人员配备相关',
                 'jianzaoshi', 'jsfzr', 'gongchengshi', 'jigong', 'sanleirenyuan', 'tezhonggong', 'ohter',
                 css_class='unsort',
                 ),
    )

    def set_form_obj_requird(self):
        if self.required_update_or_add in self.request.get_full_path() and self.user.department != "交付总监":
            for field in self.required_fields:
                self.form_obj.fields[field].required = True

    def get_btns(self):
        bnt1_per, bnt1_text = get_tupple(self.obj, messagesender.PG_FINISH_AND_FLOWTO_KF)
        bnt2_per, bnt2_text = get_tupple(self.obj, messagesender.DISPENSE_TO_JFYG)
        bnt3_per, bnt3_text = get_tupple(self.obj, messagesender.FLOW_TO_LGZJ)
        d_text = "将手动修改该进度表收结状态，请核实后点击确认！"

        btns = [
            {'text': '点击已办结',
             'candialog': True,
             'd_title': '手动更新收结状态',
             'd_hasper': bnt1_per,
             'd_text': bnt1_text,
             'd_url': self.get_submit_url(messagesender.PG_FINISH_AND_FLOWTO_KF),
             'has_msg': False,
             },
            {'text': '分发做单人',
             'candialog': True,
             'd_title': '分发给当前做单人',
             'd_hasper': bnt2_per,
             'd_text': bnt2_text,
             'd_url': self.get_submit_url(messagesender.DISPENSE_TO_JFYG),
             'has_msg': True,
             },
            {'text': '推送给猎管',
             'candialog': True,
             'd_title': '推送给猎管部门进行办理',
             'd_hasper': bnt3_per,
             'd_text': bnt3_text,
             'd_url': self.get_submit_url(messagesender.FLOW_TO_LGZJ),
             'has_msg': True,
             },
            {'text': '返回列表页',
             'candialog': False,
             'd_url': self.obj.get_model_url('list'),
             },
        ]
        return btns

    def has_change_permission(self, obj=None):
        codename = get_permission_codename('change', self.opts)
        perm = super().has_change_permission(obj)
        if obj:
            perm = self.user.is_superuser or (perm and not obj.isfinish)
        return perm

@adminx_register
class Costmodel(Baseadminmodel):
    mymodel = Cost
    hidden_menu = True
    aggregate_fields = {"money": "sum"}
class Equipment_barInline(object):
    model = Equipment_bar
    extra = 1
    # fields=['equipment','major_type','subject_or_worktype','level','ohter','number','sc_number','money','comment']
    form_layout = (
        Fieldset((u''),
                 'equipment',
                 'major_type', 'subject_or_worktype',
                 'level', 'ohter', 'personel',
                 Row('number', 'sc_number', 'money'),
                 Row('specific', 'comment'),
                 css_class='unsort notitle'
                 ),
    )

@adminx_register
class Equipmentmoel(Baseadminmodel):
    inlines = [Equipment_barInline]
    is_add_eb_persmodal = True
    mymodel = Equipment
    list_filter = mymodel.get_fields() + Prgsheet.get_fields(True) + Contract.get_fields(True)
    ordering = ['-updatetime']
    model_icon = 'fa fa-list'
    form_layout = (
        Fieldset((u''),
                 'prgsheet', 'owner', 'contract', 'comment',
                 Row('total_number', 'sc_total_number', 'total_money', 'isfinish'),
                 Row('createtime', 'updatetime', 'finishtime'), 'finishtime_recorde',
                 css_class='unsort notitle'
                 ),
    )

    def get_btns(self):
        bnt1_per, bnt1_text = get_tupple(self.obj, messagesender.EP_FINISH_AND_FLOWTO_JF)
        bnt2_per, bnt2_text = get_tupple(self.obj, messagesender.DISPENSE_TO_LGYG)
        btns = [
            {'text': '点击已配齐',
             'candialog': True,
             'd_title': '手动更新配齐状态',
             'd_hasper': bnt1_per,
             'd_text': bnt1_text,
             'd_url': self.get_submit_url(messagesender.EP_FINISH_AND_FLOWTO_JF),
             'has_msg': True,
             },
            {'text': '分发配单人',
             'candialog': True,
             'd_title': '分发给当前配单人',
             'd_hasper': bnt2_per,
             'd_text': bnt2_text,
             'd_url': self.get_submit_url(messagesender.DISPENSE_TO_LGYG),
             'has_msg': True,
             },
            {'text': '返回列表页',
             'candialog': False,
             'd_url': self.obj.get_model_url('list'),
             },
        ]
        return btns

    def save_models(self):  # 保存时生成合同
        obj = self.new_obj
        obj.contract = obj.prgsheet.contract
        obj.save()

    def get_media(self):
        path = self.request.get_full_path()
        media = super().get_media()
        if "add" in path or "update" in path:
            media = media + self.vendor('xadmin.utils.personnel_choose.js')
        return media

class Subjectmodel:
    hidden_menu = True
    only_admin_show = True
    list_display = ['id', 'name']
    ordering = ['-id']
xadmin.site.register(Subject, Subjectmodel)

class Equipment_barmodel:
    hidden_menu = True
    list_display = ['major_type', 'subject_or_worktype', 'level', 'ohter', 'number', 'sc_number', 'money', 'personel',
                    'specific']
    aggregate_fields = {"number": "sum", "sc_number": "sum", "money": "sum"}
    form_layout = (
        Fieldset((u''),
                 'equipment',
                 'major_type', 'subject_or_worktype',
                 'level', 'ohter', 'personel',
                 Row('number', 'sc_number', 'money'),
                 Row('specific', 'comment'),
                 css_class='unsort notitle'
                 ),
    )
xadmin.site.register(Equipment_bar, Equipment_barmodel)
