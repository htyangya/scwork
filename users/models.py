from django.contrib.auth.models import AbstractUser
from django.db import models
class Company(models.Model):
    name=models.CharField("公司名称",max_length=200,unique=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分公司管理'
        verbose_name_plural = verbose_name


# Create your models here.
class UserProfile(AbstractUser):
    gender_choices = (
        ('male','男'),
        ('female','女')
    )
    nick_name = models.CharField('昵称',max_length=50,default='')
    birthday = models.DateField('生日',null=True,blank=True)
    gender = models.CharField('性别',max_length=10,choices=gender_choices,default='male')
    adress = models.CharField('地址',max_length=100,default='',blank=True)
    mobile = models.CharField('手机号',max_length=11,blank=True)
    department=models.CharField('部门',max_length=50,blank=True)
    company=models.ForeignKey(Company,on_delete=models.PROTECT,verbose_name="所属分公司",default=1)
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.nick_name}({self.department})'
