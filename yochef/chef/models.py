from django.db import models
from public.models import RegionDetail
from customer.models import Like

# datetimefield를 yy.mm.dd로 바꿔주는 함수
def turn_strdate(date):
	return str(date.year) + '.' + str(date.month) + '.' + str(date.day)

# Create your models here.
class Chef(models.Model):
	customer = models.OneToOneField('customer.Customer', on_delete=models.CASCADE)
	nickname = models.CharField(max_length=20, null=True)
	spec = models.TextField(max_length=5000, null=True)
	snsLink = models.TextField(max_length = 500, null=True)
	blogLink = models.TextField(max_length = 500, null=True)
	youtubeLink = models.TextField(max_length = 500, null=True)
	registerDate = models.DateTimeField(auto_now_add=True)
	region = models.IntegerField(null=True)
	regionDetail = models.ForeignKey(RegionDetail, null=True, on_delete=models.SET_NULL)
	isLicensed = models.BooleanField(default=False)
	isSubmitted = models.BooleanField(default=False)

	def __str__(self):
		return self.nickname
	def like_count(self) :
		return Like.objects.filter(chef=self).count()

class Post(models.Model):
	chef = models.OneToOneField(Chef, on_delete=models.CASCADE)
	region = models.IntegerField(null=True)
	regionDetail = models.ForeignKey(RegionDetail, null=True, on_delete=models.SET_NULL)
	title = models.TextField(max_length=255, null=True)
	introduce = models.TextField(max_length=5000, null=True)
	spec = models.TextField(max_length=5000, null=True)
	category = models.IntegerField(null=True)		# 한식, 일식, 중식, 아시안, 양식, 채식
	notice = models.TextField(max_length=5000, null=True)
	movingPrice = models.IntegerField(default=0)
	isOpen = models.BooleanField(default=True)
	registerDate = models.DateTimeField(auto_now=True)

	def __str__(self):
		if len(self.title) > 10 :
			return self.chef.nickname + ' - ' + self.title[:10] + '...'
		else:
			return self.chef.nickname + ' - ' + self.title

	def category_name(self):
		if self.category == 1 :
			return '뷔페/케이터링'
		elif self.category == 2 :
			return '한식'
		elif self.category == 3 :
			return '일식'
		elif self.category == 4 :
			return '중식'
		elif self.category == 5 :
			return '아시안'
		elif self.category == 6 :
			return '양식'
		elif self.category == 7 :
			return '채식'
		else :
			return '기타'

class Course(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	title = models.TextField(max_length=1000)
	description = models.TextField(max_length=5000, null=True)
	price = models.IntegerField()

	def __str__(self):
		return self.title + ' - ' + str(self.price) + '원'
	
class Schedule(models.Model):	
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	# eventDate = models.DateField()
	status = models.IntegerField()	# 0: 대기  1: 예약 가능  2: 마감  3: 종료  4: 취소

	def __str__(self):
		return self.post.title + ' [' + turn_strdate(self.startTime) + '~' + turn_strdate(self.endTime) + ']'
