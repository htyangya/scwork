# Generated by Django 2.2 on 2019-06-26 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lieguan', '0004_auto_20190626_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='num',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='身份证号'),
        ),
    ]
