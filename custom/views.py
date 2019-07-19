import json
from django.http import HttpResponse
from contract.models import *

from .utils import getinfos,getcustomname
def getdata(request):
    query_str=request.GET.get('name')
    customs=getcustomname(query_str)
    data={}
    if not query_str:
        data["errorcode"]=u"没有查询公司名"
        return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json")
    try:
        data=getinfos(query_str)
    except ValueError as  e:
        data={"errorcode":e.__str__()}
    if customs:data["customs"]=customs
    return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json")
