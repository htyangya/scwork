# Generated by Django 2.2 on 2019-06-03 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('custom', '0001_initial'),
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prgsheet',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='当前做单人'),
        ),
        migrations.AddField(
            model_name='equipment_bar',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.Equipment', verbose_name='配备记录'),
        ),
        migrations.AddField(
            model_name='equipment_bar',
            name='subject_or_worktype',
            field=models.ForeignKey(blank=True, help_text='如果没有您想要的专业/工种请点击右边的+添加', null=True, on_delete=django.db.models.deletion.PROTECT, to='contract.Subject', verbose_name='工种/专业'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='contract',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contract.Contract', verbose_name='合同'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='配备人'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='prgsheet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contract.Prgsheet', verbose_name='进度表'),
        ),
        migrations.AddField(
            model_name='cost',
            name='prgsheet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.Prgsheet', verbose_name='进度表'),
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_contact',
            field=models.ForeignKey(blank=True, help_text='若本合同为其他合同的补充合同或解除合同，可以选此关联到原始合同', null=True, on_delete=django.db.models.deletion.PROTECT, to='contract.Contract', verbose_name='关联原始合同'),
        ),
        migrations.AddField(
            model_name='contract',
            name='custom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom.Custom', verbose_name='客户名称'),
        ),
    ]
