# Generated by Django 3.2.5 on 2021-07-14 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chef', '0015_rename_permit_status_schedule_confirm_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='spec',
        ),
    ]