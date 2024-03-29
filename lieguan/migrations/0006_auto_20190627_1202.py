# Generated by Django 2.2 on 2019-06-27 12:02

import datetime
from django.db import migrations, models
import lieguan.models


class Migration(migrations.Migration):

    dependencies = [
        ('lieguan', '0005_auto_20190626_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='enddate',
            field=models.DateField(default=lieguan.models._nextyeardate, verbose_name='合同到期日期'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='signdate',
            field=models.DateField(default=datetime.date.today, verbose_name='合同签订日期'),
        ),
    ]
