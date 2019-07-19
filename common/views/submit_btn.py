from django.http import HttpResponse
from django.shortcuts import redirect
from common.utils import get_obj_from_request
from django.contrib import messages
from common.messagesender import submit_done

def flow_view(request):
    model,obj=get_obj_from_request(request)
    msg=request.GET.get('msg',None)
    type=request.GET['type']
    type=int(type)
    respond,code=submit_done(obj,type,msg)
    if respond:
        messages.info(request,  '您的推送操作已经处理成功，请在下面的通知栏查看详情！')
    else:
        messages.error(request, code)

    return redirect(model.model_url+f"/{obj.id}/detail")
