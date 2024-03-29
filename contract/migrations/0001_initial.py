# Generated by Django 2.2 on 2019-06-03 12:18

import contract.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='合同名称')),
                ('num', models.CharField(help_text='注意，该编号不能重复', max_length=200, unique=True, verbose_name='合同编号')),
                ('singman', models.CharField(blank=True, max_length=200, verbose_name='签单人')),
                ('signdate', models.DateField(default=datetime.date(2019, 6, 3), verbose_name='签单日期')),
                ('year', models.CharField(default=2019, max_length=4, verbose_name='年度')),
                ('total_price', models.IntegerField(verbose_name='合同金额（元）')),
                ('contract_type', models.CharField(choices=[('资质合同', '资质合同'), ('工商', '工商'), ('工商注销', '工商注销'), ('解除合同', '解除合同'), ('补充合同', '补充合同'), ('食品经营', '食品经营'), ('条形码', '条形码'), ('代理记账', '代理记账'), ('人力资源', '人力资源'), ('认证服务', '认证服务'), ('网站开发', '网站开发'), ('人力资源', '人力资源'), ('商标', '商标'), ('委托协议', '委托协议'), ('培训协议', '培训协议'), ('LOGO设计', 'LOGO设计'), ('人才协议', '人才协议'), ('专利合同', '专利合同'), ('企业咨询', '企业咨询'), ('著作权', '著作权'), ('专利合同', '专利合同')], default='资质合同', max_length=200, verbose_name='合同分类')),
                ('comment', models.TextField(blank=True, help_text='合同注意事项可以填写此处', verbose_name='合同备注')),
                ('update_by', models.CharField(choices=[('管理员脚本上传', '管理员脚本上传'), ('网站生成', '网站生成')], default='网站生成', max_length=200, verbose_name='数据生成方式')),
                ('file', models.FileField(blank=True, null=True, upload_to=contract.models.contract_path, verbose_name='相关附件')),
                ('itemcontent', models.TextField(blank=True, verbose_name='项目具体内容')),
                ('payment', models.TextField(blank=True, verbose_name='付款方式')),
                ('deadline', models.IntegerField(blank=True, help_text='填写该合同最长的期限时间，以工作日为单位，详细描述填写到下一个字段', null=True, verbose_name='合同期限（工作日）')),
                ('deadline_text', models.CharField(blank=True, help_text='填写期限描述，例如分阶段的期限', max_length=200, verbose_name='合同期限详细描述')),
                ('deadline_date', models.DateField(blank=True, help_text='请根据合同期限填写截止日期，所有超期未办结的资质类单子将在首页进行提醒', null=True, verbose_name='合同截止时间')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('finishtime', models.DateTimeField(blank=True, null=True, verbose_name='收结时间')),
                ('Accepted', models.IntegerField(default=0, verbose_name='收款单.已收')),
                ('receivable', models.IntegerField(default=0, verbose_name='收款单.未收')),
                ('isfinish', models.BooleanField(default=False, verbose_name='是否收结')),
            ],
            options={
                'verbose_name': '合同',
                'verbose_name_plural': '合同',
                'permissions': (('viewall_contract', 'Can 查看所有合同'), ('viewcompany_contract', 'Can 查看分公司所有合同'), ('vewowner_contract', 'Can 查看个人合同'), ('export_contract', 'Can 导出合同')),
            },
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='培训费/公关费等', max_length=200, verbose_name='费用类型')),
                ('forwhat', models.CharField(help_text='用于什么公司的什么费用', max_length=200, verbose_name='费用事由')),
                ('money', models.IntegerField(verbose_name=' 费用金额(元)')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '成本单',
                'verbose_name_plural': '成本单',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isfinish', models.BooleanField(default=False, verbose_name='是否配齐')),
                ('comment', models.TextField(blank=True, help_text='工作进度和特殊说明应填写此处', verbose_name='备注说明')),
                ('total_number', models.IntegerField(default=0, verbose_name='总人数')),
                ('sc_total_number', models.IntegerField(default=0, verbose_name='首涂需提供总人数')),
                ('total_money', models.IntegerField(default=0, verbose_name='总费用')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('finishtime', models.DateTimeField(blank=True, null=True, verbose_name='最后配齐时间')),
                ('finishtime_recorde', models.CharField(default='{}', max_length=300, verbose_name='配齐时间记录')),
            ],
            options={
                'verbose_name': '猎管：配备记录',
                'verbose_name_plural': '猎管：配备记录',
                'permissions': (('viewall_equipment', 'Can 查看所有配备记录'), ('viewcompany_equipment', 'Can 查看分公司所有配备记录'), ('vewowner_equipment', 'Can 查看个人配备记录'), ('export_equipment', 'Can 导出配备记录')),
            },
        ),
        migrations.CreateModel(
            name='Equipment_bar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_type', models.CharField(choices=[('建造师', '建造师'), ('技术负责人', '技术负责人'), ('工程师', '工程师'), ('现场管理人员', '现场管理人员'), ('技工', '技工'), ('特种工', '特种工'), ('三类人员', '三类人员'), ('其他注册类人员', '其他注册类人员'), ('其他', '其他')], max_length=200, verbose_name='所属大类')),
                ('level', models.CharField(blank=True, choices=[('初级', '初级'), ('中级', '中级'), ('高级', '高级'), ('一级', '一级'), ('二级', '二级'), ('三级', '三级'), ('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=200, verbose_name='级别/证书级别')),
                ('ohter', models.CharField(blank=True, max_length=200, verbose_name='年限或其他描述')),
                ('number', models.IntegerField(default=0, verbose_name='总人数')),
                ('sc_number', models.IntegerField(default=0, verbose_name='首涂需提供人数')),
                ('money', models.IntegerField(default=0, verbose_name='费用')),
                ('specific', models.CharField(blank=True, max_length=300, verbose_name='具体人员姓名')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='备注说明')),
            ],
            options={
                'verbose_name': '配备条',
                'verbose_name_plural': '配备条',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='专业/工种')),
            ],
            options={
                'verbose_name': '专业/工种',
                'verbose_name_plural': '专业/工种',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_type', models.CharField(choices=[(0, '收款'), (1, '退款')], default=0, max_length=10, verbose_name='收款/退款')),
                ('pay_by', models.CharField(choices=[('现金', '现金'), ('银行转账', '银行转账'), ('电子支付', '电子支付'), ('其他', '其他')], default='银行转账', max_length=10, verbose_name='收款方式')),
                ('pay_dep', models.CharField(help_text='请填写对方打款具体银行及汇款帐号，电子支付填写微信/支付宝等应用名称', max_length=50, verbose_name='银行帐号/机构名称')),
                ('pay_info', models.CharField(blank=True, help_text='如有必要,可填写对方汇款信息,包括对方姓名、身份证号等', max_length=200, verbose_name='汇款信息')),
                ('money', models.IntegerField(verbose_name='收款金额(元)')),
                ('received_acount', models.CharField(choices=[(0, '贵州银行'), (1, '贵州银行8243'), (2, '贵州银行510'), (3, '工商银行624'), (4, '建设银行')], default=0, max_length=50, verbose_name='收款帐号')),
                ('pay_description', models.CharField(help_text='请填写收款信息，比如首笔款、进度款等', max_length=200, verbose_name='收款描述')),
                ('received_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='实际收款时间')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.Contract', verbose_name='合同')),
            ],
            options={
                'verbose_name': '财务：收款单',
                'verbose_name_plural': '财务：收款单',
                'permissions': (('viewall_receipt', 'Can 查看所有收款单'), ('viewcompany_receipt', 'Can 查看分公司所有收款单'), ('vewowner_receipt', 'Can 查看个人收款单'), ('export_receipt', 'Can 导出收款单')),
            },
        ),
        migrations.CreateModel(
            name='Prgsheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ownerrecord', models.CharField(blank=True, help_text='做单人存在更换情况在此记录', max_length=200, verbose_name='做单人记录')),
                ('approval_dep', models.CharField(blank=True, max_length=200, verbose_name='审批部门')),
                ('approval_address', models.CharField(blank=True, max_length=200, verbose_name='审批部门地址')),
                ('type', models.CharField(blank=True, help_text='资质申请业务（新办/增项/升级）', max_length=200, verbose_name='资质类别')),
                ('progress', models.CharField(blank=True, help_text='未启动/已启动/差安证/差增项/已退单/已办结等', max_length=200, verbose_name='办理进度')),
                ('prg_explain', models.TextField(blank=True, verbose_name='进度说明')),
                ('isfinish', models.BooleanField(default=False, verbose_name='是否办结')),
                ('ispropelling', models.BooleanField(default=False, verbose_name='是否通知猎管配人')),
                ('file', models.FileField(blank=True, null=True, upload_to=contract.models.prgsheet_path, verbose_name='相关附件')),
                ('jianzaoshi', models.TextField(blank=True, help_text='注明：级别、专业、人数', verbose_name='建造师')),
                ('jsfzr', models.TextField(blank=True, help_text='注明：职称级别、专业、工程管理经历年限、人数', verbose_name='技术负责人')),
                ('gongchengshi', models.TextField(blank=True, help_text='注明：专业、人数', verbose_name='工程师')),
                ('xcglry', models.TextField(blank=True, help_text='注明：专业、人数', verbose_name='现场管理人员')),
                ('jigong', models.TextField(blank=True, help_text='注明：级别、工种、人数', verbose_name='技工')),
                ('tezhonggong', models.TextField(blank=True, help_text='注明：级别、工种、人数', verbose_name='特种工')),
                ('ohter', models.TextField(blank=True, help_text='其他人员', verbose_name='其他')),
                ('totalcost', models.IntegerField(default=0, verbose_name='成本汇总')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('finishtime', models.DateTimeField(blank=True, null=True, verbose_name='办结时间')),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contract.Contract', verbose_name='合同')),
            ],
            options={
                'verbose_name': '交付：进度表',
                'verbose_name_plural': '交付：进度表',
                'permissions': (('viewall_prgsheet', 'Can 查看所有进度表'), ('viewcompany_prgsheet', 'Can 查看分公司所有进度表'), ('vewowner_prgsheet', 'Can 查看个人进度表'), ('export_prgsheet', 'Can 导出进度表')),
            },
        ),
    ]
