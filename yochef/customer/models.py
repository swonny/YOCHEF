from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
from public.models import *

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	region = models.IntegerField()
	regionDetail = models.ForeignKey(RegionDetail, null=True, on_delete=models.SET_NULL)
	nickname = models.CharField(max_length=20)
	email = models.EmailField(null=True)
	phoneNum = models.CharField(max_length=11)
	point = models.IntegerField(default=0)
	isChef = models.BooleanField(default=False)
	registerDate = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nickname
		

class Coupon(models.Model):
	title = models.TextField(max_length=255)
	description = models.TextField(max_length=1000) 
	validDate = models.DateTimeField()
	offrate = models.IntegerField(null=True)

	def __str__(self):
		return self.title + ' - ' + str(self.offrate) + '%off'

class HasCoupon(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	isUsed = models.BooleanField(default=False)

	def __str__(self):
		return self.customer.nickname + '님 - ' + self.coupon.title

class VerifyNum(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	verifyNum = models.IntegerField()

	def __str__(self):
		return self.customer.nickname + '의 인증번호 : ' + str(self.verifyNum)

class Like(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	chef = models.ForeignKey('chef.Chef', on_delete=models.CASCADE)

	def __str__(self):
		return self.customer.nickname + ' likes ' + self.chef.nickname

class Book(models.Model):
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	coupon = models.ForeignKey(Coupon, null=True, on_delete=models.SET_NULL)
	schedule = models.ForeignKey('chef.Schedule', null=True, on_delete=models.SET_NULL)
	status = models.IntegerField()
	phoneNum = models.CharField(max_length=11)
	usedPoint = models.IntegerField()
	payMethod = models.IntegerField()
	totalPrice = models.IntegerField()
	personNum = models.IntegerField()
	comment = models.TextField(max_length=1000, null=True)
	registerDate = models.DateTimeField(auto_now=True) 

	def __str__(self):
		return self.schedule.post.chef.nickname + ' 셰프 - ' + self.customer.nickname

class BookDetail(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	course = models.ForeignKey('chef.Course', null=True, on_delete=models.SET_NULL)
	amount = models.IntegerField()

	def __str__(self):
		return self.course.title + ' - ' + str(self.amount) + '개'


class Review(models.Model):
	post = models.ForeignKey('chef.Post', on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	pubdate = DateTimeField(auto_now=True)
	description = models.TextField(max_length=5000)

	def __str__(self):
		if len(self.description) > 20 :
			return '[' + self.customer.nickname + '] ' + self.description[:20] + '...'
		else :
			return '[' + self.customer.nickname + '] ' + self.description
