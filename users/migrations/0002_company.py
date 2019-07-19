# Generated by Django 2.2 on 2019-06-03 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='公司名称')),
            ],
            options={
                'verbose_name': '分公司管理',
                'verbose_name_plural': '分公司管理',
            },
        ),
    ]