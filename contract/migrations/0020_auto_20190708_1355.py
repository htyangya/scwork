# Generated by Django 2.2 on 2019-07-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0019_auto_20190705_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prgsheet',
            name='progress',
            field=models.CharField(blank=True, default=None, help_text='未启动/已启动/差安证/差增项/已退单/已办结等', max_length=200, null=True, verbose_name='办理进度'),
        ),
    ]
