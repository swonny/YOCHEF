from django.urls import path
from .views import *
urlpatterns = [
	path('', main, name='main'),
	path('changePageVer/', changePageVer, name='changePageVer'),
	path('postList', postList, name="postList"),
	path('detail/<int:post_id>', detail, name="detail"),
	path('getRegion', getRegionAPI, name="getRegion"),
	path('getRegionDetail', getRegionDetailAPI, name="getRegionDetail"),
	path('changeFile', changeFile, name="changeFile")
]