from django.urls import path
from . import views

urlpatterns = [
    path('registerChef/<int:page_num>', views.registerChef, name="registerChef"),
    path('chefSchedule/', views.chefSchedule, name="chefSchedule"),
    path('chefSchedule/<int:schedule_id>', views.chefScheduleDetail, name="chefScheduleDetail"),
    path('chefSchedule/<int:schedule_id>/confirm', views.scheduleConfirm, name="scheduleConfirm"),
    path('editChefProfile/', views.editChefProfile, name="editChefProfile"),
    path('editChefProfile/update', views.updateChefProfile, name="updateChefProfile"),
]