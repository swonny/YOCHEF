# Generated by Django 3.2.3 on 2021-06-26 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('public', '0001_initial'),
        ('customer', '0003_hascoupon_verifynum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=20)),
                ('spec', models.TextField(max_length=5000)),
                ('snslink', models.TextField(max_length=500, null=True)),
                ('blogLink', models.TextField(max_length=500, null=True)),
                ('youtubeLink', models.TextField(max_length=500, null=True)),
                ('chefPhoneNum', models.CharField(max_length=11)),
                ('registerDate', models.DateTimeField(auto_now_add=True)),
                ('region', models.IntegerField()),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('regionDetail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.regiondetail')),
            ],
        ),
    ]