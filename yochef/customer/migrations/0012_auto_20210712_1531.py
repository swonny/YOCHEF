# Generated by Django 3.2.5 on 2021-07-12 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20210712_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='nickname',
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(default='standard', max_length=50),
            preserve_default=False,
        ),
    ]
