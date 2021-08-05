# Generated by Django 3.2.5 on 2021-08-05 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0011_rename_specorder_file_order'),
        ('chef', '0021_course_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='region',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='regionDetail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.regiondetail'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]