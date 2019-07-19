import xadmin
from xadmin.views import BaseAdminPlugin
from xadmin.views.detail import DetailAdminView
from xadmin.views.edit import CreateAdminView,UpdateAdminView

class Getdata(BaseAdminPlugin):
    is_execute = False

    def init_request(self, *args, **kwargs):
        return bool(self.is_execute)
    def get_context(self, context):
        return context
    def get_media(self, media):
        path = self.request.get_full_path()
        current_uri = '{scheme}://{host}'.format(scheme=self.request.scheme, host=self.request.get_host())
        if "add" in path or "update" in path :
            media = media + self.vendor('xadmin.utils.getdata.js')
        return media

    def block_before_fieldsets(self, context, nodes):
        return '<button class="btn btn-primary" type="button" onclick="getdata()">根据客户名称查询企查查信息</button>'
xadmin.site.register_plugin(Getdata, CreateAdminView)
xadmin.site.register_plugin(Getdata, UpdateAdminView)