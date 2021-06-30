# Generated by Django 3.2.3 on 2021-06-28 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef', '0004_auto_20210627_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='registerDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='chef',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]