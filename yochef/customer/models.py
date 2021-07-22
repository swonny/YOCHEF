from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
from public.models import *

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	email = models.EmailField(null=True)
	phoneNum = models.CharField(max_length=11)
	point = models.IntegerField(default=0)
	isChef = models.BooleanField(default=False)
	registerDate = models.DateTimeField(auto_now_add=True)
	currentVer = models.IntegerField(default=0)

	def __str__(self):
		return self.name
		
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
		return self.customer.name + '님 - ' + self.coupon.title

class VerifyNum(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	verifyNum = models.IntegerField()

	def __str__(self):
		return self.customer.name + '의 인증번호 : ' + str(self.verifyNum)

class Like(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	chef = models.ForeignKey('chef.Chef', on_delete=models.CASCADE)

	def __str__(self):
		return self.customer.name + ' likes ' + self.chef.nickname

# 조회수 관련 모델 - 보류
# class View(models.Model):
# 	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
# 	post = models.ForeignKey('chef.Post', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return self.customer.nickname + ' likes ' + self.chef.nickname

class Book(models.Model):
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	coupon = models.ForeignKey(Coupon, null=True, on_delete=models.SET_NULL)
	schedule = models.ForeignKey('chef.Schedule', on_delete=models.CASCADE)
	paymentStatus = models.IntegerField(default=1)	# 1: 예약가능  2: 예약됨  3. 취소됨
	phoneNum = models.CharField(max_length=11)
	usedPoint = models.IntegerField(null=True)
	payMethod = models.IntegerField(null=True)
	course = models.ForeignKey('chef.Course', null=True, on_delete=models.SET_NULL)
	totalPrice = models.IntegerField(null=True)
	personNum = models.IntegerField()
	comment = models.TextField(max_length=1000, null=True)
	registerDate = models.DateTimeField(auto_now=True) 

	def __str__(self):
		return self.schedule.post.chef.nickname + ' 셰프 - ' + self.course.title

	def print_paymentStatus(self):
		if self.paymentStatus == 1:
			return "예약가능"
		elif self.paymentStatus == 2:
			return "예약됨"
		elif self.paymentStatus == 3:
			return "취소됨"
		else:
			return "Error"

class Review(models.Model):
	post = models.ForeignKey('chef.Post', on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	pubdate = DateTimeField(auto_now=True)
	description = models.TextField(max_length=5000)

	def __str__(self):
		if len(self.description) > 20 :
			return '[' + self.customer.name + '] ' + self.description[:20] + '...'
		else :
			return '[' + self.customer.name + '] ' + self.description
