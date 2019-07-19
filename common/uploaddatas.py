import pandas as pd
from django.shortcuts import redirect,HttpResponse

from contract.models import *

def uploaddatas(request):
    file = r"C:\Users\Administrator\Desktop\工作资料\EXCEL已阅\file.xlsx"
    df = pd.read_excel(file)
    df.fillna("",inplace=True)
    df['signdate'] = pd.to_datetime(df['signdate'])
    df['year']=df['year'].astype(str)
    custom_list = ['name', 'city', 'contact_man', 'tel','founder_id','company_id']
    contract_list = [ 'Cname','num','singman', 'signdate', 'year', 'total_price', 'contract_type', 'update_by',
                      'itemcontent', 'payment', 'deadline_text']
    prg_list = ['owner','ownerrecord', 'progress', 'prg_explain']

    # if contractname=Cname:contractfield='name'

    for index, row in df.iterrows():
        customs=Custom.objects.filter(name=row['name'])
        if customs:
            custom=customs.all()[0]
        else:
            custom=Custom()
            for each in custom_list:
                setattr(custom,each,row[each])
            custom.save()
        contracts=Contract.objects.filter(num=row['num'])
        if contracts:
            contract=contracts.all()[0]
        else:
            contract=Contract(name=row['Cname'],custom=custom)
            for each in contract_list[1:]:
                setattr(contract,each,row[each])
            contract.save()
        if not Prgsheet.objects.filter(contract=contract):
            prgsheet=Prgsheet(contract=contract,ownerrecord=row['ownerrecord'],
                              progress=row['progress'],prg_explain=row['prg_explain'],
                              owner=UserProfile.objects.get(nick_name=row['owner'])
                              )
            prgsheet.save()

    return  HttpResponse("sucessful!")


def uploadcontract(request):
    file = r"C:\Users\Administrator\Desktop\2019商标类合同电子档.xlsx"
    df = pd.read_excel(file)
    df.fillna("",inplace=True)
    df['signdate'] = pd.to_datetime(df['signdate'])
    df['year']=df['year'].astype(str)
    custom_list = ['name','contact_man', 'tel','founder_id','company_id']
    contract_list = [ 'Cname','num','singman', 'signdate', 'year', 'total_price', 'contract_type', 'update_by',
                      ]
    for index, row in df.iterrows():
        customs=Custom.objects.filter(name=row['name'])
        if customs:
            custom=customs.all()[0]
        else:
            custom=Custom()
            for each in custom_list:
                setattr(custom,each,row[each])
            custom.save()
        contracts=Contract.objects.filter(num=row['num'])
        if contracts:
            contract=contracts.first()
            if contract.custom!=custom:contract.custom=custom
            if contract.name!=row['Cname']:contract.name=row['Cname']
            for each in contract_list[1:]:
                if getattr(contract, each)!=row[each]:setattr(contract, each, row[each])
            contract.save()
        else:
            contract=Contract(name=row['Cname'],custom=custom)
            for each in contract_list[1:]:
                setattr(contract,each,row[each])
            contract.save()

    return  HttpResponse("sucessful!")

def  _get_or_create_subjects(names):
    subjects = []
    for subject_str in names.split(','):
        subject,created=Subject.objects.get_or_create(name=subject_str)
        subjects.append(subject)
    return subjects

def uploadpersonel():
    from lieguan.models import Personnel
    file = r"C:\Users\Administrator\Desktop\personel.xlsx"
    df = pd.read_excel(file, converters={'tel': str, 'num': str})
    df.fillna("", inplace=True)
    df['signdate'] = pd.to_datetime(df['signdate'])
    df['enddate'] = pd.to_datetime(df['enddate'])
    personel_list =['name','num','gender','contact_man','tel','major_type','level','money','singman','signdate','enddate'
]
    mtm='subject_or_worktype'
    i=0
    for index, row in df.iterrows():
        personel=Personnel.objects.filter(name=row['name'],major_type=row['major_type'])
        if personel.exists():
            pass
        else:
            i=i+1
            personel=Personnel()
            for each in personel_list:
                if isinstance(row[each],str):
                    value=row[each].strip()
                else:
                    value=row[each]
                setattr(personel,each,value)
            personel.founder_id=1
            personel.save()
            subjects=_get_or_create_subjects(row['subject_or_worktype'])
            if subjects:personel.subject_or_worktype.add(*subjects)

    return  "sucessful!"+str(i)

def update_b_for_personnel():
    from lieguan.models import Personnel
    file = r"C:\Users\Administrator\Desktop\contract_subject.xlsx"
    df = pd.read_excel(file)
    df.fillna("", inplace=True)
    i=0
    for index, row in df.iterrows():
        personel = Personnel.objects.filter(name__contains=row['name'], major_type=row['major_type'],level=row['level'])

        if personel.exists():
            i=i+1
            for p in personel:
                p.subject_or_worktype.add(Subject.objects.get(name='B'))
        else:
            print(row['name'])
    return "success"+str(i)



def test():
    file = r"C:\Users\Administrator\Desktop\personel.xlsx"
    df = pd.read_excel(file,converters={'tel':str,'num':str})
    df.fillna("", inplace=True)
    df['signdate'] = pd.to_datetime(df['signdate'])
    df['enddate'] = pd.to_datetime(df['enddate'])

    return df