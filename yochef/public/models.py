from django.db import models

# Create your models here.
class Qna(models.Model):
	category = models.IntegerField()
	description = models.TextField(max_length=5000)
	email = models.EmailField()
	isChecked = models.BooleanField(default=False)

class RegionDetail(models.Model):
	detailName = models.CharField(max_length=20)
	region = models.IntegerField()

class File(models.Model):
	attachment = models.FileField()
	category = models.IntegerField()
	chef = models.ForeignKey('chef.Chef', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('chef.Post', on_delete=models.CASCADE, null=True)
	course = models.ForeignKey('chef.Course', on_delete=models.CASCADE, null=True)
	specOrder = models.IntegerField(null=True)
