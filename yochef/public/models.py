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
		return str(self.region) + ' - ' + self.detailName

class File(models.Model):
	attachment = models.FileField()
	category = models.IntegerField() # 1. chef profile, 2. chef spec, 3. course image, 4. post cover image
	chef = models.ForeignKey('chef.Chef', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('chef.Post', on_delete=models.CASCADE, null=True)
	course = models.ForeignKey('chef.Course', on_delete=models.CASCADE, null=True)
	specOrder = models.IntegerField(null=True)
