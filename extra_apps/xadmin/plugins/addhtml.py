import os

import xadmin
from xadmin.views import BaseAdminPlugin
from xadmin.views.detail import DetailAdminView
from xadmin.views.edit import CreateAdminView,UpdateAdminView
from scwork.settings import BASE_DIR
#添加equipment的配备条 人才选择项的modal模态选择框
class Add_modal(BaseAdminPlugin):
    is_add_eb_persmodal = False

    def init_request(self, *args, **kwargs):
        return bool(self.is_add_eb_persmodal )
    def get_context(self, context):
        return context
    # def get_media(self, media):
    #     path = self.request.get_full_path()
    #     current_uri = '{scheme}://{host}'.format(scheme=self.request.scheme, host=self.request.get_host())
    #     if "add" in path or "update" in path :
    #         media = media + self.vendor('xadmin.utils.getdata.js')
    #     return media


    def block_mymodal(self, context, nodes):
        html=os.path.join(BASE_DIR,"extra_apps/xadmin/templates/xadmin/personnel_choose/choose_modal.html")
        return open(html,"r",encoding='utf8').read()
xadmin.site.register_plugin(Add_modal, CreateAdminView)
xadmin.site.register_plugin(Add_modal, UpdateAdminView)