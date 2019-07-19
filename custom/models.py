from django.db import models
from django.utils.safestring import mark_safe

from common.middlewares import get_current_user,get_current_company
from users.models import UserProfile, Company
from common.basemodel import Basemodel

class Custom(Basemodel):
    list_display=['get_option_html','name','address','city','contact_man','tel','contract_count','company','createtime','updatetime']
    readonly_fields = ['createtime', 'updatetime','founder','company']
    search_fields = ['name']
    name=models.CharField("客户名称",max_length=200,unique=True)
    address=models.CharField("客户地址",max_length=200,blank=True)
    city=models.CharField("所属城市",max_length=200,blank=True)
    contact_man = models.CharField("联系人", max_length=200,blank=True)
    tel=models.CharField("电话号码",max_length=50,blank=True)
    comment=models.TextField("客户备注",blank=True)
    createtime=models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("修改时间", auto_now=True)
    founder = models.ForeignKey(UserProfile, verbose_name="创建人", on_delete=models.PROTECT,default=get_current_user)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="所属分公司",default=get_current_company)

    # test.short_description="测试"
    def get_third_fields(self):
        fields=self.get_fields()
        return [ "contract__custom__"+field for field in fields]

    def contract_count(self):
        count=self.contract_set.all().count()
        if count:
            return mark_safe(f"<a href='/contract/contract/?_rel_custom__id__exact={self.id}'>{count}</a>")
        return  count
    contract_count.short_description="合同数量"

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = verbose_name
        permissions = (
            ("viewall_custom", "Can 查看所有客户"),
            ("viewcompany_custom", "Can 查看分公司所有客户"),
            ("vewowner_custom", "Can 查看个人客户"),
            ("export_custom", "Can 导出客户"),
        )
    def __str__(self):
        return self.name
Custom.set_model_infos()
class Notify(Basemodel):
    list_display = ['title','type']
    search_fields = ['title']
    type = models.CharField("类型", max_length=1,default=0)
    title=models.CharField("标题", max_length=200)
    text=models.TextField("内容")

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-id']
        verbose_name = '通知管理'
        verbose_name_plural = verbose_name

