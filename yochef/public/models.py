from django.db import models

# Create your models here.
class Qna(models.Model):
	category = models.IntegerField()
	description = models.TextField(max_length=5000)
	email = models.EmailField()
	isChecked = models.BooleanField(default=False)

	def __str__(self):
		# 카테고리 확정 시 수정
		if len(self.description) > 20 :
			return self.description[:20] + '...'
		else :
			return self.description

class RegionDetail(models.Model):
	detailName = models.CharField(max_length=20)
	region = models.IntegerField()

	def __str__(self):
		# 지역 번호별 항목 확정 시 수정 
		return '[' + str(self.id) + '] ' + str(self.region) + ' - ' + self.detailName 

class File(models.Model):
	attachment = models.FileField(upload_to='media')
	category = models.IntegerField() # 1. chef profile, 2. chef spec, 3. course image, 4. post cover image
	chef = models.ForeignKey('chef.Chef', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('chef.Post', on_delete=models.CASCADE, null=True)
	course = models.ForeignKey('chef.Course', on_delete=models.CASCADE, null=True)
	order = models.IntegerField(null=True) # 파일 입력 순서
	uploadDate = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)

	def print_category(self):
		if self.category == 1:
			return "1. chef profile"
		elif self.category == 2:
			return "2. chef spec"
		elif self.category == 3:
			return "3. course Image"
		elif self.category == 4:
			return "4. post cover Image"
		return

	def print_uploadDate(self):
		t = ['일', '월', '화', '수', '목', '금', '토']
		return self.uploadDate.strftime("%Y.%m.%d") + " " + t[int(self.uploadDate.strftime("%w"))]