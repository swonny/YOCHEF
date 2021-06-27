from django.db import models
from public.models import RegionDetail

# Create your models here.
class Chef(models.Model):
	customer = models.OneToOneField('customer.Customer', on_delete=models.CASCADE)
	nickname = models.CharField(max_length=20)
	spec = models.TextField(max_length=5000, null=True)
	snslink = models.TextField(max_length = 500, null=True)
	blogLink = models.TextField(max_length = 500, null=True)
	youtubeLink = models.TextField(max_length = 500, null=True)
	chefPhoneNum = models.CharField(max_length=11)
	registerDate = models.DateTimeField(auto_now_add=True)
	region = models.IntegerField()
	regionDetail = models.ForeignKey(RegionDetail, null=True, on_delete=models.SET_NULL)

class Post(models.Model):
	chef = models.OneToOneField(Chef, on_delete=models.CASCADE)
	region = models.IntegerField()
	regionDetail = models.ForeignKey(RegionDetail, null=True, on_delete=models.SET_NULL)
	title = models.TextField(max_length=255)
	introduce = models.TextField(max_length=5000)
	spec = models.TextField(max_length=5000, null=True)
	category = models.IntegerField()
	notice = models.TextField(max_length=5000)
	movingPrice = models.IntegerField(default=0)
	isOpen = models.BooleanField(default=True)

class Course(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	title = models.TextField(max_length=1000)
	description = models.TextField(max_length=5000, null=True)
	price = models.IntegerField()
	
class Schedule(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	status = models.IntegerField()
