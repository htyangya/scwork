from django.db import models
from contract.models import *
from django.utils.safestring import mark_safe


class zizhireport(Contract):
    list_display = ['name', 'custom_tel', 'custom_city', 'custom_contact_man',
                    'singman', 'signdate', 'year', 'total_price', 'Accepted', 'receivable', 'isfinish',
                    'deadline', 'deadline_date',
                    'prgsheet_owner', 'prgsheet_type',
                    'prgsheet_progress', 'prgsheet_isfinish', 'prgsheet_ispropelling', 'prgsheet_totalcost',
                    'equipment_owner', 'equipment_total_number', 'equipment_sc_total_number', 'equipment_total_money',
                    'equipment_isfinish',
                    'profit'
                    ]
    search_fields = ['num', 'name', 'custom__name']

    def custom_name(self):
        return self.custom.name

    custom_name.short_description = "客户名称"
    custom_name.value_format = True

    def custom_tel(self):
        return self.custom.tel

    custom_tel.short_description = "客户电话"

    def custom_city(self):
        return self.custom.city

    custom_city.short_description = "客户城市"
    custom_city.value_format = True

    def custom_contact_man(self):
        return self.custom.contact_man

    custom_contact_man.short_description = "客户联系人"
    custom_contact_man.value_format = True

    # 以下是进度表字段
    def prgsheet_owner(self):
        return self.prgsheet.owner

    prgsheet_owner.short_description = "当前做单人"

    def prgsheet_ownerrecord(self):
        return self.prgsheet.ownerrecord

    prgsheet_ownerrecord.short_description = "做单人记录"
    prgsheet_ownerrecord.value_format = True

    def prgsheet_approval_dep(self):
        return self.prgsheet.approval_dep

    prgsheet_approval_dep.short_description = "审批部门"
    prgsheet_approval_dep.value_format = True

    def prgsheet_type(self):
        return self.prgsheet.type

    prgsheet_type.short_description = "资质类别"
    prgsheet_type.value_format = True

    def prgsheet_progress(self):
        return self.prgsheet.progress

    prgsheet_progress.short_description = "办理进度"
    prgsheet_progress.value_format = True

    def prgsheet_isfinish(self):
        return self.prgsheet.isfinish

    prgsheet_isfinish.short_description = "是否办结"
    prgsheet_isfinish.boolean = True

    def prgsheet_totalcost(self):
        return self.prgsheet.totalcost

    prgsheet_totalcost.short_description = "成本汇总"

    def prgsheet_ispropelling(self):
        return self.prgsheet.ispropelling

    prgsheet_ispropelling.short_description = "是否通知猎管配人"
    prgsheet_ispropelling.boolean = True

    # 以下是配备记录
    def equipment_owner(self):
        return self.equipment.owner

    equipment_owner.short_description = "配备人"

    def equipment_isfinish(self):
        return self.equipment.isfinish

    equipment_isfinish.short_description = "是否配齐"
    equipment_isfinish.boolean = True

    def equipment_total_number(self):
        return self.equipment.total_number

    equipment_total_number.short_description = "总人数"

    def equipment_sc_total_number(self):
        return self.equipment.sc_total_number

    equipment_sc_total_number.short_description = "首途需提供总人数"

    def equipment_total_money(self):
        return self.equipment.total_money

    equipment_total_money.short_description = "总费用"

    def equipment_comment(self):
        return self.equipment.comment

    equipment_comment.short_description = "配备说明"
    equipment_comment.value_format = True

    def profit(self):
        return self.Accepted - self.equipment.total_money - self.prgsheet.totalcost

    profit.short_description = "利润结余"

    class Meta:
        verbose_name = '资质类业务专用报表'
        verbose_name_plural = verbose_name
        proxy = True
        permissions = (
            ("export_zizhireport", "Can 导出资质类专用报表"),
        )
