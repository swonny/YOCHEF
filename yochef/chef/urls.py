from django.urls import path
from . import views

urlpatterns = [
    path('registerChef/<int:page_num>', views.registerChef, name="registerChef"),
    path('chefSchedule/', views.chefSchedule, name="chefSchedule"),
    path('chefSchedule/<int:schedule_id>', views.chefScheduleDetail, name="chefScheduleDetail"),
    path('chefProfile/', views.chefProfile, name="chefProfile"),
    path('chefProfile/save', views.chefProfileSave, name="chefProfileSave"),
]