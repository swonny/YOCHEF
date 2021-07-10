from django.contrib import admin
from .models import *

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'nickname', 'region']
    list_display_links = ['id', 'customer', 'nickname']
    list_per_page = 20

# Register your models here.
#admin.site.register(Chef)
admin.site.register(Post)
admin.site.register(Course)
admin.site.register(Schedule)