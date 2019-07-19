import requests,re,cpca
from pyquery import PyQuery as pq
from custom.models import Custom

headers = {
'Host':'www.qichacha.com',
'User-Agent':r'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Accept':'*/*',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding':'gzip, deflate',
'Referer':'http://www.qichacha.com/',
'Connection':'keep-alive',
'If-Modified-Since':'Wed, 30 **********',
'If-None-Match':'"59*******"',
'Cache-Control':'max-age=0',
'Cookie': r'zg_did=%7B%22did%22%3A%20%2215fa403cb9d15f-036a7756df6645-173b7740-100200-15fa403cb9e2c6%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201510617843749%2C%22updated%22%3A%201510626410277%2C%22info%22%3A%201510285233062%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22f62f1e8a5eaa98a4fdd7be63f003baf3%22%7D; UM_distinctid=15fa403d33a86-04e900fd4e3572-173b7740-100200-15fa403d33b3d; CNZZDATA1254842228=770755339-1510283630-https%253A%252F%252Fwww.baidu.com%252F%7C1510623074; _uab_collina=151028523773154434859974; _umdata=2BA477700510A7DFF3E360D067D6CBF26EBF4D0B7616E2F668ACF5B05BA3A15BB7B2A5C9048062DECD43AD3E795C914C698D4F63619694FD3C24BCCF0E0016EF; PHPSESSID=tm27c7utiff9j5iqbh4g1cg0l5; acw_tc=AQAAAIyPMmgK2AUA4oumtwogJ3fbLlic; hasShow=1'
}

def getinfos(str):
    querystr = "https://www.qichacha.com/search?key="
    dict = {}
    dict['原公司名称'] = str
    r=requests.get(querystr+str,headers=headers)
    doc=pq(r.text)
    num=doc('#countOld > span').text()
    if r.status_code!=200 or not num:raise ValueError(u'查询过多，本日IP已被企查查禁用')
    if int(num.strip())==0:raise ValueError(u'没有找到相关公司名称')
    infos=doc('#search-result > tr:nth-child(1) > td:nth-child(3)')
    a=infos('a')
    infos_str=infos.text()+chr(10)#把最后一行也加一个换行符，方便用正则匹配

    dict['查找到公司名称']=a.text().split(' ')[0]
    for item in ['负责人','法定代表人','注册资本','成立时间','邮箱','电话','地址']:
        resp=re.search(f'{item}：\s?(.+?)\s', infos_str)
        if resp:
            dict[item]=re.search(f'{item}：\s?(.+?)\s',infos_str).group(1)
        else:
            dict[item] =''

    if  "贵安"  in dict['地址']:
        dict['城市'] = "贵安新区"
    else:
        df = cpca.transform([dict['地址']])
        dict['城市'] = df.loc[0, '市'] + df.loc[0, '区']
    return dict

def getcustomname(str):
    return list(Custom.objects.filter(name__contains=str).values_list('name'))

