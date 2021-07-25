from django.contrib import admin
from .models import *

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'nickname']
    list_display_links = ['customer', 'nickname']
    list_per_page = 20

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'chef', 'title', 'category_name', 'movingPrice', 'isOpen', 'registerDate']
    list_display_links = ['chef', 'title', 'category_name', 'movingPrice', 'isOpen', 'registerDate']
    list_per_page = 20

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'title', 'print_description', 'price']
    list_display_links = ['post', 'title', 'print_description', 'price']
    list_per_page = 20

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'eventDate', 'eventTime', 'print_confirmStatus']
    list_display_links = ['post', 'eventDate', 'eventTime', 'print_confirmStatus']
    list_per_page = 20


# Register your models here.
#admin.site.register(Chef)
#admin.site.register(Post)
#admin.site.register(Course)
#admin.site.register(Schedule)