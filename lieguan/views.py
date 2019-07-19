import json
from .utils import pack_personnel_qs
from .models import Personnel
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def personnelsview(request):
    major_type= request.POST.get("major_type") or request.GET.get("major_type")
    level=request.POST.get("level") or request.GET.get("level")
    subject=request.POST.get("subject") or request.GET.get("subject")
    id_list=request.POST.get("id_list") or request.GET.get("id_list")
    type = request.POST.get("type") or request.GET.get("type")
    if id_list:id_list=json.loads(id_list)
    if major_type=="技术负责人":
        major_type="工程师"
    elif major_type=="三类人员" and (level or subject):
        major_type=None
        subject=level or subject
        level=None
    data=pack_personnel_qs(Personnel.filter(major_type,level,subject,id_list,type))
    return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json")
