# Generated by Django 2.2 on 2019-06-06 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_company_pro_userprofile_pro'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company_pro',
            options={'verbose_name': '分公司管理', 'verbose_name_plural': '分公司管理'},
        ),
        migrations.AlterModelOptions(
            name='userprofile_pro',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
    ]