# Generated by Django 2.2 on 2019-07-05 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lieguan', '0009_auto_20190703_1625'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personnel',
            options={'ordering': ['updatetime'], 'permissions': (('viewall_personnel', 'Can 查看所有猎管人才'), ('viewcompany_personnel', 'Can 查看分公司所有猎管人才'), ('vewowner_personnel', 'Can 查看个人猎管人才'), ('export_personnel', 'Can 导出猎管人才'), ('info_personnel', 'Can 查看人才所有信息')), 'verbose_name': '猎聘人才', 'verbose_name_plural': '猎聘人才'},
        ),
        migrations.AlterModelOptions(
            name='personnel_rc',
            options={'permissions': (('viewall_personnel_rc', 'Can 查看所有人才使用记录'), ('viewcompany_personnel_rc', 'Can 查看分公司所有人才使用记录'), ('vewowner_personnel_rc', 'Can 查看个人人才使用记录'), ('export_personnel_rc', 'Can 导出人才使用记录')), 'verbose_name': '人才使用记录', 'verbose_name_plural': '人才使用记录'},
        ),
        migrations.RenameField(
            model_name='personnel_rc',
            old_name='isconcel',
            new_name='iscancel',
        ),
        migrations.AddField(
            model_name='personnel_rc',
            name='canceltime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='修改时间'),
        ),
    ]