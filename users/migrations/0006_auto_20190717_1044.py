# Generated by Django 2.2 on 2019-07-17 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190606_1725'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Company_pro',
        ),
        migrations.DeleteModel(
            name='UserProfile_pro',
        ),
    ]
