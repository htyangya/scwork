# Generated by Django 2.2 on 2019-06-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0005_notify'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notify',
            options={'verbose_name': '通知管理', 'verbose_name_plural': '通知管理'},
        ),
        migrations.AlterField(
            model_name='notify',
            name='type',
            field=models.CharField(default=0, max_length=1, verbose_name='类型'),
        ),
    ]