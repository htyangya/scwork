from django.db.models import Q
import  xadmin,time
from xadmin.layout import Fieldset,Row
from .models import Personnel,Personnel_rc
from common.basemodel import Baseadminmodel as Bm,adminx_register


class Baseadminmodel(Bm):
    ordering = ['-updatetime']
    def queryset(self):
        qs = super(Baseadminmodel, self).queryset()
        modelname=self.model_info[1]
        # qs = qs.filter(contract_type="资质合同", prgsheet__ispropelling=True)  # 筛选
        params={}
        if modelname in ['personnel','personnel_rc']:
            #属于五种基本过滤类型，判断权限进i行筛选
            viewall=self.user.has_perm('%s.viewall_%s' % self.model_info)
            viewcompany=self.user.has_perm('%s.viewcompany_%s' % self.model_info)
            viewowner=self.user.has_perm('%s.viewowner_%s' % self.model_info)
            company=self.user.company
            user=self.user
            params_viewcompany = {'personnel': {'company':company},
                                  'personnel_rc':{'personnel__company':company},
                                  }
            params_viewowner = Q(equipment_bar__equipment__prgsheet__owner=user)| Q(equipment_bar__equipment__owner=user)

            if viewall:
                pass
            elif viewcompany:
                params=params_viewcompany.get(modelname)
                qs=qs.filter(**params)
            else:
                qs=qs.filter(params_viewowner)

        return qs

@adminx_register
class Personneladmin(Baseadminmodel):
    mymodel = Personnel
    list_prefetch_related = ['equipment_bar_set__equipment__prgsheet__contract','subject_or_worktype']
    model_icon = 'fa fa-book'
    list_filter = ['subject_or_worktype__name','equipment_bar__equipment__prgsheet__contract']+mymodel.get_fields()
    list_editable=['canreuse','islive']
    form_layout = (
        Fieldset((u'猎聘人才'),
                 Row('name', 'num','gender'),
                 Row('contact_man', 'tel'),
                 'major_type', 'subject_or_worktype', 'level', 'money', 'singman',
                 Row('islive', 'canreuse'),
                  Row('signdate', 'enddate'),

                  'comment',
                 Row('createtime', 'updatetime', 'founder','company'),
                 css_class='unsort'),
        Fieldset('相关附件',
                 Row('file', 'file_to_pdf'),
                 Row('zsfile', 'zsfile_to_pdf'),
        ),
    )

    #在get_context之前，修改list_exclude数据
    def get_context(self):
        caninfo=self.user.has_perm('%s.info_%s' % self.model_info)
        if not caninfo:self.list_exclude=['contact_man','tel','money','file','file_to_pdf']
        return super().get_context()

    #这是detail/add/update/get的第一个操作，使用工厂制造一个modelform类，
    # 在这个操作更改后面要使用的exclude和form_layout
    def get_model_form(self, **kwargs):
        caninfo = self.user.has_perm('%s.info_%s' % self.model_info)
        if  (not caninfo) and (not "add" in self.request.get_full_path()):
            self.exclude=['contact_man','tel','money','file','file_to_pdf']
            self.form_layout=(
            Fieldset((u'猎聘人才'),
                     Row('name', 'num','gender'),
                     'major_type', 'subject_or_worktype', 'level',  'singman',
                     Row('islive', 'canreuse'),
                      Row('signdate', 'enddate'),
                      'comment',
                     Row('createtime', 'updatetime', 'founder','company'),
                     css_class='unsort'),
            Fieldset('相关附件',
                     Row('zsfile', 'zsfile_to_pdf'),
                    ),
            )
        return super().get_model_form( **kwargs)

@adminx_register
class Personnel_rc_admin(Baseadminmodel):
    mymodel = Personnel_rc
    list_editable=['iscancel']
    model_icon = 'fa fa-list'
