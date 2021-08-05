from django.contrib import admin
from .models import *

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'customer']
    list_display_links = ['id', 'nickname', 'customer']
    list_per_page = 20

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category_name', 'movingPrice', 'region_name', 'isOpen', 'print_registerDate', 'chef']
    list_display_links = ['id', 'title', 'category_name', 'movingPrice', 'region_name', 'isOpen', 'print_registerDate', 'chef']
    list_per_page = 20

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'print_description', 'price', 'post']
    list_display_links = ['id', 'title', 'print_description', 'price', 'post']
    list_per_page = 20

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'print_eventDate', 'eventTime', 'region', 'regionDetail', 'print_confirmStatus']
    list_display_links = ['id', 'post', 'print_eventDate', 'eventTime', 'region', 'regionDetail', 'print_confirmStatus']
    list_per_page = 20


# Register your models here.
#admin.site.register(Chef)
#admin.site.register(Post)
#admin.site.register(Course)
#admin.site.register(Schedule)