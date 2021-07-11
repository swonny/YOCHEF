from django.contrib import admin
from .models import *

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'nickname', 'region']
    list_display_links = ['customer', 'nickname', 'region']
    list_per_page = 20

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'chef', 'title', 'category', 'movingPrice', 'isOpen', 'registerDate']
    list_display_links = ['chef', 'title', 'category', 'movingPrice', 'isOpen', 'registerDate']
    list_per_page = 20

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'title', 'description', 'price']
    list_display_links = ['post', 'title', 'description', 'price']
    list_per_page = 20

    def description(self, course):
        return course.description[:20] + '...'

    def price(self, course):
        return str(course.price) + " KRW"

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'startTime', 'endTime', 'status']
    list_display_links = ['post', 'startTime', 'endTime', 'status']
    list_per_page = 20

    def status(self, schedule):
        if schedule.status == 0:
            return "0: 대기"
        elif schedule.status == 1:
            return "1: 예약 가능"
        elif schedule.status == 2:
            return "2: 예약 마감"
        elif schedule.status == 3:
            return "3: 종료"
        elif schedule.status == 4:
            return "4: 취소"
        else:
            return schedule.status


# Register your models here.
#admin.site.register(Chef)
#admin.site.register(Post)
#admin.site.register(Course)
#admin.site.register(Schedule)