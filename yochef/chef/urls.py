from django.urls import path
from . import views

urlpatterns = [
    path('registerchef/<int:page_num>', views.registerChef, name="registerChef"),
    path('chefSchedule/', views.chefSchedule, name="chefSchedule"),
    path('chefSchedule/detail', views.chefScheduleDetail, name="chefScheduleDetail"),
]