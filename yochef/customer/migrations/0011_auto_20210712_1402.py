# Generated by Django 3.2.5 on 2021-07-12 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chef', '0013_auto_20210712_1402'),
        ('customer', '0010_auto_20210710_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chef.course'),
        ),
        migrations.AlterField(
            model_name='book',
            name='schedule',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='chef.schedule'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='BookDetail',
        ),
    ]
