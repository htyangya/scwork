from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from contract import apps
from .models import *

class Base_resource(resources.ModelResource):
    def __init__(self):
        super().__init__()
        # 获取所以字段的verbose_name并存放在字典
        field_list = UserProfile._meta.fields
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



class Userresource(Base_resource):
     # company=Field(column_name="所属分公司", attribute="company", widget=ForeignKeyWidget(Company, 'name'))
     class Meta:
        model = UserProfile
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('username',)
        fields = ['username','password','nick_name','first_name','department',"company",'gender', 'is_staff','is_active']
        export_order =fields




