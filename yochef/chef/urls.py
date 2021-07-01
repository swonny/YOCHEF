from django.urls import path
from . import views

urlpatterns = [
    path('registerChef/<int:page_num>', views.registerChef, name="registerChef"),
]