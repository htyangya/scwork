# Generated by Django 2.2 on 2019-06-03 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190603_1317'),
        ('custom', '0003_delete_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.Company', verbose_name='所属分公司'),
        ),
    ]
