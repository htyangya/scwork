import datetime
import os
from django.apps import apps

from common.middlewares import get_current_user

def set_file_path(instance, filename,modelname,typename):
    num = str(instance)
    year = datetime.date.today().year
    moon = datetime.date.today().month
    type = typename + os.path.splitext(filename)[-1]
    return f'{modelname}/{year}/{moon}/{num}_{type}'

#过长文字缩短显示
def format_value(value):
    value=value[:15]+"..."if(len(value)>15) else value

def format_value_has_link(v,length,url=None):
    if len(v) > length:
        if url:
            re=f"<a href={url}>{v[:length]}</a><em><a onclick='toggle_value(this)' hidevalue={v[length:]} style='color:red'>...</a></em>"
        else:
            re = f"<span>{v[:length]}</span><em><a class='hidden-link' onclick='toggle_value(this) ' hidevalue={v[length:]} style='color:red'>...</a></em>"
    else:
        if url:
            re=f"<a href={url}>{v}</a>"
        else:
            re=f"<span>{v}</span>"
    return re

def get_obj_from_request(request):
    app_label=request.GET['app_label']
    model_name=request.GET['model_name']
    id=request.GET['id']
    return get_obj(app_label,model_name,id)

def get_obj(app_label,model_name,id):
    model=apps.get_model(app_label,model_name,False)
    obj=model.objects.get(pk=id)
    return model,obj