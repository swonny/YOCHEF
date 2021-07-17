# Generated by Django 3.2.5 on 2021-07-14 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chef', '0017_auto_20210714_1559'),
        ('public', '0008_auto_20210710_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='chef',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chef.chef'),
        ),
        migrations.AlterField(
            model_name='file',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chef.course'),
        ),
        migrations.AlterField(
            model_name='file',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chef.post'),
        ),
        migrations.AlterField(
            model_name='file',
            name='specOrder',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]