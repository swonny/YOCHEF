from django.urls import path
from .views import *
urlpatterns = [
	path('', main, name='main'),
	path('changePageVer/', changePageVer, name='changePageVer'),
]