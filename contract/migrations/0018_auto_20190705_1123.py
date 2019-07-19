# Generated by Django 2.2 on 2019-07-05 11:23

import contract.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import functools


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contract', '0017_auto_20190703_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='founder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prgsheet',
            name='file_to_pdf',
            field=models.BooleanField(default=True, verbose_name='转化为PDF'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='founder',
            field=models.ForeignKey(default=81, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prgsheet',
            name='file',
            field=models.FileField(blank=True, help_text='勾选转化为PDF，会将默认将上传的zip压缩包转化为pdf，请确认压缩包格式为zip，并且压缩包中的图片格式为pnp或jpg', null=True, upload_to=functools.partial(contract.models.set_file_path, *(), **{'modelname': 'prgsheet', 'typename': '进度表附件'}), verbose_name='相关附件'),
        ),
    ]
