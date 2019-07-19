from django.forms import Form

import  xadmin
from .models import Custom,Notify
from contract.models import Contract
from common.basemodel import Baseadminmodel
from xadmin import views

class Custommodel(Baseadminmodel):
    mymodel = Custom
    is_execute=True
    list_prefetch_related= ['contract_set']
    model_icon = 'fa fa-users'
    ordering = ['-updatetime']
Custommodel.set_settings()

class Notifyadmin(Baseadminmodel):
    ordering = ['-id']
    mymodel = Notify
    list_display = mymodel.list_display
    search_fields = mymodel.search_fields
    readonly_fields = mymodel.readonly_fields
    list_filter = mymodel.get_fields()
xadmin.site.register(Notify,Notifyadmin)

class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

xadmin.site.register(views.BaseAdminView,BaseSetting)

class GlobalSetting(object):
    #页头
    site_title = '首途业务资源管理系统'
    #页脚
    site_footer = '首途CRM（备案号：黔ICP备19004636号-1）'
    # menu_style = 'accordion'
xadmin.site.register(views.CommAdminView, GlobalSetting)