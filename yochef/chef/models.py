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
	isLicensed = models.BooleanField(default=False)
	isSubmitted = models.BooleanField(default=False)

	def __str__(self):
		if self.nickname:
			return self.nickname
		else:
			return "Chef Object:" + str(self.id)

	def like_count(self) :
		return Like.objects.filter(chef=self).count()

class Post(models.Model):
	chef = models.OneToOneField(Chef, on_delete=models.CASCADE)
	region = models.IntegerField(null=True)
	regionDetail = models.ForeignKey(RegionDetail, null=True, on_delete=models.SET_NULL)
	title = models.TextField(max_length=255, null=True)
	introduce = models.TextField(max_length=5000, null=True)
	category = models.IntegerField(null=True)		# 한식, 일식, 중식, 아시안, 양식, 채식
	notice = models.TextField(max_length=5000, null=True)
	movingPrice = models.IntegerField(default=0)
	isOpen = models.BooleanField(default=True)
	registerDate = models.DateTimeField(auto_now=True)

	def __str__(self):
		if self.title:
			return self.title
		else:
			return "Post Object:" + str(self.id)

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

	def region_name(self):
		if self.region == 1:
			return "서울"
		elif self.region == 2:
			return "경기"
		elif self. region == 3:
			return "인천"
		elif self. region == 4:
			return "부산"
		elif self. region == 5:
			return "경상, 대구, 울산"
		elif self. region == 6:
			return "대전, 충청"
		elif self. region == 7:
			return "강원"
		elif self. region == 8:
			return "광주, 전라, 제주"

	def print_registerDate(self):
		t = ['일', '월', '화', '수', '목', '금', '토']
		return self.registerDate.strftime("%Y.%m.%d") + " " + t[int(self.registerDate.strftime("%w"))] + " " + self.registerDate.strftime("%I:%M:%S")

class Course(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	title = models.TextField(max_length=1000)
	description = models.TextField(max_length=5000, null=True, blank=True)
	price = models.IntegerField()
	order = models.IntegerField(null=True)  # 등록된 순서

	def __str__(self):
		if self.title:
			return self.title
		else:
			return "Course Object: " + str(self.id)

	def print_description(self):
		if self.description == None:
			return None
		elif len(self.description) > 50:
			return self.description[:50] + '...'
		else:
			return self.description
	
class Schedule(models.Model):	
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	eventDate = models.DateField()
	eventTime = models.CharField(max_length=100, null=True)
	confirmStatus = models.IntegerField(default=0)	# 0: '-'(결제전)  1: 승인대기  2: 승인됨  3. 취소됨
	region = models.IntegerField(null=True, blank=True)
	regionDetail = models.ForeignKey(RegionDetail, null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.post.title + "일정" + str(self.id)

	def print_confirmStatus(self):
		if self.confirmStatus == 0:
			return "-"
		elif self.confirmStatus == 1:
			return "승인대기"
		elif self.confirmStatus == 2:
			return "승인됨"
		elif self.confirmStatus == 3:
			return "취소됨"
		else:
			return "Error"

	def print_eventDate(self):
		t = ['일', '월', '화', '수', '목', '금', '토']
		return self.eventDate.strftime("%Y.%m.%d") + " " + t[int(self.eventDate.strftime("%w"))]

	def print_eventDateDay(self):
		t = ['일', '월', '화', '수', '목', '금', '토']
		return t[int(self.eventDate.strftime("%w"))]