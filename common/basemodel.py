from django.db import models
from django.db.models import Q, Count
from django.utils.safestring import mark_safe
import xadmin
from common.middlewares import get_current_user
from common import utils


class Basemodel(models.Model):
    readonly_fields = []
    list_display = []
    search_fields = []

    @classmethod
    def get_fields(cls, includmodelname=False):
        fieldsobj = cls._meta.fields
        if includmodelname:
            modelname = cls.__name__.lower()
            return [modelname + '__' + field.name for field in fieldsobj if field.name != 'id']
        else:
            return [field.name for field in fieldsobj]

    class Meta:
        abstract = True

    def get_model_url(self, name):
        if not hasattr(self, 'model_url'): self.__class__.set_model_infos()
        if name == "list":
            url = self.model_url + f"/?_p_id__in={self.id}"
        elif name == "detail":
            url = self.model_url + f"/{self.id}/detail/"
        else:
            url = self.model_url + f"/{self.id}/update/"
        return url

    def get_model_link(self, name, length=10):
        url = self.get_model_url(name)
        re = utils.format_value_has_link(str(self), length, url)
        return mark_safe(re)

    @classmethod
    def set_model_infos(cls):
        cls.app_label = cls._meta.app_label
        cls.model_name = cls._meta.model_name
        cls.model_info = cls.app_label, cls.model_name
        cls.model_url = f'/{cls.app_label}/{cls.model_name}'
        return cls.model_name

    def get_notify_status(self, type):
        qs = self.notifies.filter(type=type)
        if not qs: return "全部已读"
        qs = qs.values('status').annotate(scount=Count('status'))
        waitsend = 0
        send = 0
        readed = 0
        status = ""
        for dict in qs:
            if dict['status'] == "待发送":
                waitsend = dict['scount']
            elif dict['status'] == "已发送":
                send = dict['scount']
            elif dict['status'] == "已读":
                readed = dict['scount']

        if waitsend > 0:
            status = "等待发送"
        elif send > 0:
            status = "等待已读"
        else:
            status = "全部已读"
        return status

    def get_option_html(self):
        cls = self.__class__
        if not hasattr(cls, "model_info"): return "空"
        detail_link = "<a href='{url}/{id}/detail/'><span class='fa fa-folder-open'></span></a>".format(
            url=self.model_url, id=self.id)
        update_link = "<a href='{url}/{id}/update/'><span class='glyphicon glyphicon-edit'></span></a>".format(
            url=self.model_url, id=self.id)
        user = get_current_user()
        if user.has_perm('%s.change_%s' % self.model_info):
            return mark_safe(detail_link + "&nbsp;" + update_link)
        return mark_safe(detail_link)

    get_option_html.short_description = "操作"


myclass = ['custom', 'contract', 'receipt', 'prgsheet', 'equipment']


def model_meta_register(cls):
    if hasattr(cls, 'set_model_infos'):
        cls.set_model_infos()
    return cls


class Baseadminmodel:
    required_fields = []
    list_editable = []
    list_display_links_details = False
    required_update_or_add = "update"
    list_prefetch_related = None
    list_select_related = None
    list_per_page = 15
    list_item_max_length = 10
    list_max_exclude_field = []
    relfield_style = 'fk-ajax'
    list_display = []
    readonly_fields = []
    search_fields = []
    list_filter = []
    show_detail_fields = []
    model_icon = ''
    aggregate_fields = []
    inlines = []
    ordering = []
    hidden_menu = False
    only_admin_show = False
    mymodel = None

    @classmethod
    def set_settings(cls):
        mymodel = cls.mymodel
        cls.list_display = mymodel.list_display
        cls.search_fields = mymodel.search_fields
        cls.readonly_fields = mymodel.readonly_fields
        if not cls.list_filter: cls.list_filter = mymodel.get_fields()
        if not cls.show_detail_fields: cls.show_detail_fields = [cls.list_display[0]]
        xadmin.site.register(mymodel, cls)

    def set_form_obj_requird(self):
        if self.required_update_or_add in self.request.get_full_path():
            for field in self.required_fields:
                self.form_obj.fields[field].required = True

    def queryset(self):
        qs = super(Baseadminmodel, self).queryset()
        modelname = self.model_info[1]
        # qs = qs.filter(contract_type="资质合同", prgsheet__ispropelling=True)  # 筛选
        params = {}
        if modelname in myclass:
            # 属于五种基本过滤类型，判断权限进i行筛选
            viewall = self.user.has_perm('%s.viewall_%s' % self.model_info)
            viewcompany = self.user.has_perm('%s.viewcompany_%s' % self.model_info)
            viewowner = self.user.has_perm('%s.viewowner_%s' % self.model_info)
            company = self.user.company
            user = self.user
            params_viewcompany = {'custom': {'company': company},
                                  'contract': {'custom__company': company},
                                  'receipt': {'contract__custom__company': company},
                                  'prgsheet': {'contract__custom__company': company},
                                  'equipment': {'contract__custom__company': company},
                                  }
            params_viewowner = {'custom': Q(contract__prgsheet__owner=user) | Q(contract__equipment__owner=user),
                                'contract': Q(prgsheet__owner=user) | Q(equipment__owner=user),
                                'receipt': Q(contract__prgsheet__owner=user) | Q(contract__equipment__owner=user),
                                'prgsheet': Q(owner=user) | Q(equipment__owner=user),
                                'equipment': Q(owner=user) | Q(prgsheet__owner=user),
                                }
            if viewall:
                pass
            elif viewcompany:
                params = params_viewcompany.get(modelname)
                qs = qs.filter(**params)
            else:
                qs = qs.filter(params_viewowner.get(modelname))

        return qs


def adminx_register(cls):
    if hasattr(cls, 'set_settings'):
        cls.set_settings()
    return cls
