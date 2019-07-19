from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from contract import apps
from .models import *

class Prg_base_resource(resources.ModelResource):
    contract = Field(column_name="合同编号", attribute="contract", widget=ForeignKeyWidget(Contract, 'name'))

    def __init__(self):
        super(Prg_base_resource, self).__init__()
        # 获取所以字段的verbose_name并存放在字典
        field_list = Prgsheet._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields



class Prg_ex_resource(Prg_base_resource):
     contract__custom__city=Field(column_name="城市", attribute="contract__custom__city")
     class Meta:
        model = Prgsheet
        fields = ['contract','contract__custom__city','ownerrecord', 'owner', 'approval_dep', 'approval_address',
                  'type', 'progress','prg_explain' ,'isfinish','ispropelling','totalcost','file',
         'createtime','updatetime','finishtime']
        export_order =fields

class Prg_im_resource(Prg_base_resource):

    class Meta:
        model = Prgsheet
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('contract',)
        fields = ['contract','ownerrecord', 'owner', 'approval_dep', 'approval_address',
                  'type', 'progress' ,'isfinish', 'ispropelling','prg_explain', ]


