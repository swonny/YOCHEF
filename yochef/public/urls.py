from django.urls import path
from .views import *
urlpatterns = [
	path('', main, name='main'),
	path('changePageVer/', changePageVer, name='changePageVer'),
	path('postList', postList, name="postList"),
	path('detail/<int:post_id>', detail, name="detail"),
	path('reviewDetail/<int:post_id>', reviewDetail, name="reviewDetail"),
	path('getRegion', getRegionAPI, name="getRegion"),
	path('getRegion/<int:region_id>', getRegionAPI, name="getRegion"),
	path('getRegionDetail', getRegionDetailAPI, name="getRegionDetail"),
	path('changeFile', changeFile, name="changeFile"),
	path('postLike', postLikeAPI, name="postLike"),
	path('getCoupon', getCouponAPI, name="getCoupon"),
]