# Generated by Django 3.1a1 on 2020-07-08 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20200708_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='reg_CustomerId',
            field=models.CharField(default='default', max_length=50),
        ),
        migrations.AlterField(
            model_name='registration',
            name='reg_ReferalId',
            field=models.CharField(default='default', max_length=50),
        ),
    ]