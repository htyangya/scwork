# Generated by Django 2.2 on 2019-07-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lieguan', '0011_auto_20190709_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='num',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='身份证号'),
        ),
    ]