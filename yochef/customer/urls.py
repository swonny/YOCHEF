from django.urls import path
from .views import *
urlpatterns = [
	path('login', login, name='login'),
	path('logout', logout, name='logout'),
	path('signup', signup, name='signup'),
	path('findId', findId, name='findId'),
	path('findPw', findPw, name='findPw'),
	path('createAccount', createAccount, name='createAccount'),
	path('mypage', mypage, name='mypage'),
	path('apply', apply, name='apply'),
	path('payment', payment, name='payment'),
	path('mymenuLikedmenu', mymenuLikedmenu, name='mymenuLikedmenu'), #백참고 : html 확인을 위해 작성했습니다.
	path('mymenuReservation', mymenuReservation, name='mymenuReservation'), #백참고 : html 확인을 위해 작성했습니다.
]