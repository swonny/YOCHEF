# from django.contrib import admin
# from .models import *

# # Register your models here.
# admin.site.register(Customer)
# admin.site.register(Coupon)
# admin.site.register(HasCoupon)
# admin.site.register(VerifyNum)
# admin.site.register(Like)
# admin.site.register(Book)
# admin.site.register(Review)

from django.contrib import admin
from .models import *

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'isChef', 'registerDate', 'currentVer']
    list_display_links = ['name', 'isChef', 'registerDate', 'currentVer']
    list_per_page = 20

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'validDate', 'offrate']
    list_display_links = ['id', 'title', 'validDate', 'offrate']
    list_per_page = 20

@admin.register(HasCoupon)
class HasCouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'isUsed']
    list_display_links = ['customer', 'isUsed']
    list_per_page = 20

@admin.register(VerifyNum)
class VerifyNumAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'verifyNum']
    list_display_links = ['customer', 'verifyNum']
    list_per_page = 20

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'chef']
    list_display_links = ['customer', 'chef']
    list_per_page = 20

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'coupon', 'schedule', 'print_paymentStatus', 'usedPoint', 'print_paymentMethod', 'course', 'totalPrice', 'registerDate']
    list_display_links = ['customer', 'coupon', 'schedule', 'print_paymentStatus', 'usedPoint', 'print_paymentMethod', 'course', 'totalPrice', 'registerDate']
    list_per_page = 20

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'customer', 'book', 'description']
    list_display_links = ['post', 'customer', 'book', 'description']
    list_per_page = 20