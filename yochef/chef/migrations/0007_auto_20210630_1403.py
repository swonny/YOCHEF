# Generated by Django 3.1.7 on 2021-06-30 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef', '0006_auto_20210629_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chef',
            name='chefPhoneNum',
        ),
        migrations.AddField(
            model_name='chef',
            name='isLicensed',
            field=models.BooleanField(default=False),
        ),
    ]
