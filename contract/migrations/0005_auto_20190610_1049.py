# Generated by Django 2.2 on 2019-06-10 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0004_auto_20190606_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='prgsheet',
            name='propellingtime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='通知猎管时间'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='signdate',
            field=models.DateField(default=datetime.date(2019, 6, 10), verbose_name='签单日期'),
        ),
    ]
