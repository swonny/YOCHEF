from django.urls import path
from . import views

urlpatterns = [
    path('registerChef/<int:page_num>', views.registerChef, name="registerChef"),
    path('chefSchedule/', views.chefSchedule, name="chefSchedule"),
    path('chefSchedule/update', views.addSchedule, name="addSchedule"),
    path('chefSchedule/delete', views.deleteSchedule),
    path('chefSchedule/<int:schedule_id>', views.chefScheduleDetail, name="chefScheduleDetail"),
    path('chefSchedule/<int:schedule_id>/confirm', views.scheduleConfirm, name="scheduleConfirm"),
    path('chefSchedule/<int:schedule_id>/cancel', views.scheduleCancel, name="scheduleCancel"),
    path('editChefProfile/', views.editChefProfile, name="editChefProfile"),
    path('editChefProfile/update', views.updateChefProfile, name="updateChefProfile"),
    path('editPost/', views.editPost, name="editPost"),
    path('editPost/update', views.updatePost, name="updatePost"),
    path('editMovingPrice/', views.editMovingPrice, name="editMovingPrice"),
    path('editMovingPrice/update', views.updateMovingPrice, name="updateMovingPrice"),
]