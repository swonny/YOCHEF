from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Coupon)
admin.site.register(HasCoupon)
admin.site.register(VerifyNum)
admin.site.register(Like)
admin.site.register(Book)
admin.site.register(BookDetail)
admin.site.register(Review)
