import xadmin
from contract.models import Contract,Prgsheet,Equipment
from report.models import zizhireport,Custom
from common.basemodel import Baseadminmodel
from xadmin.layout import Fieldset,Row, Main


class zizhireportmodel(Baseadminmodel):
    list_select_related=['custom','prgsheet','equipment']
    mymodel = zizhireport
    list_display = mymodel.list_display
    search_fields = mymodel.search_fields
    readonly_fields = mymodel.readonly_fields
    list_filter = mymodel.get_fields()+Custom.get_fields(True)+Prgsheet.get_fields(True)+Equipment.get_fields(True)
    show_detail_fields = [list_display[0]]
    model_icon = 'fa fa-book'

    def queryset(self):
        qs = super(zizhireportmodel, self).queryset()
        qs = qs.filter(contract_type="资质合同",equipment__createtime__isnull=False)  # 筛选
        return qs
xadmin.site.register(zizhireport,zizhireportmodel)