from .models import Personnel
#将qs包装为需要的数据，包括姓名 当前状态 专业
# ｛name:xxx,status:html,subjects:[x1,x2,x3]｝
def pack_personnel_qs(qs):
    data=[]
    if qs:
        data=[ {"id":personnel.id,
                'type':personnel.major_type+" "+personnel.level,
                'name':personnel.name,
                'money':personnel.money,
                'statushtml':personnel.get_status(),
                "subjects":[subject.name for subject in personnel.subject_or_worktype.all()]} for personnel in qs]

    return data

