# Generated by Django 2.2 on 2019-07-01 12:06

import common.middlewares
from django.db import migrations, models
import django.db.models.deletion
import functools
import lieguan.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190606_1725'),
        ('lieguan', '0007_auto_20190627_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='canreuse',
            field=models.BooleanField(default=True, help_text='建造师人才默认可重复利用，其他人才根据该字段判断，勾选则可以重复利用，否则一旦使用后，将不能在搜索框中选出此人才', verbose_name='可否重复利用'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='company',
            field=models.ForeignKey(default=common.middlewares.get_current_company, on_delete=django.db.models.deletion.PROTECT, to='users.Company', verbose_name='所属分公司'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='zsfile',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(lieguan.models.set_file_path, *(), **{'modelname': 'contract', 'typename': '合同附件'}), verbose_name='证书等其他附件'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='zsfile_to_pdf',
            field=models.BooleanField(default=True, verbose_name='转化为PDF'),
        ),
        migrations.AddField(
            model_name='personnel_rc',
            name='isconcel',
            field=models.BooleanField(default=False, verbose_name='是否已从该公司注销'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='islive',
            field=models.BooleanField(default=True, verbose_name='当前可用'),
        ),
        migrations.AlterField(
            model_name='personnel_rc',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.Contract', verbose_name='合同'),
        ),
        migrations.AlterField(
            model_name='personnel_rc',
            name='equipment_bar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.Equipment_bar', verbose_name='配备条'),
        ),
        migrations.AlterField(
            model_name='personnel_rc',
            name='personnel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lieguan.Personnel', verbose_name='人才'),
        ),
    ]