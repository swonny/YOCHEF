from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Qna)
admin.site.register(RegionDetail)
#admin.site.register(File)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'print_category', 'chef', 'post', 'course', 'attachment', 'order', 'print_uploadDate']
    list_display_links = ['id', 'print_category', 'chef', 'post', 'course', 'attachment', 'order', 'print_uploadDate']
    list_per_page = 30