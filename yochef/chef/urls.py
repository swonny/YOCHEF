from django.urls import path
from . import views

urlpatterns = [
    path('registerchef/<int:page_num>', views.registerChef, name="registerChef"),
    path('chefschedule/', views.chefSchedule, name="chefSchedule"),
    path('chefschedule/<int:schedule_id>', views.chefScheduleDetail, name="chefScheduleDetail"),
    path('chefschedule/<int:schedule_id>/confirm', views.scheduleConfirm, name="scheduleConfirm"),
    path('editchefprofile/', views.editChefProfile, name="editChefProfile"),
    path('editchefprofile/update', views.updateChefProfile, name="updateChefProfile"),
    path('editpost/', views.editPost, name="editPost"),
    path('editpost/update', views.updatePost, name="updatePost"),
    path('editmovingprice/', views.editMovingPrice, name="editMovingPrice"),
    path('editmovingprice/update', views.updateMovingPrice, name="updateMovingPrice"),
]