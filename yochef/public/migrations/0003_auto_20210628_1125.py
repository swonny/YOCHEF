# Generated by Django 3.2.3 on 2021-06-28 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_auto_20210627_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='qna',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='regiondetail',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
