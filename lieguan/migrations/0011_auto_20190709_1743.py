# Generated by Django 2.2 on 2019-07-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lieguan', '0010_auto_20190705_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='name',
            field=models.CharField(max_length=10, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='personnel_rc',
            name='canceltime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='调出时间'),
        ),
        migrations.AlterField(
            model_name='personnel_rc',
            name='iscancel',
            field=models.BooleanField(default=False, verbose_name='是否已从该公司调出'),
        ),
        migrations.AlterUniqueTogether(
            name='personnel',
            unique_together={('name', 'major_type')},
        ),
    ]