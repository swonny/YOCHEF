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
	path('payComplete', payComplete, name="payComplete"),
	path('kakaoPayLogic', kakaoPayLogic),
	path('paySuccess', paySuccess),
	path('payFail', payFail),
	path('payCancel', payCancel),
	path('mymenuLikedmenu', mymenuLikedmenu, name='mymenuLikedmenu'), 
	path('mymenuReservation', mymenuReservation, name='mymenuReservation'), 
	path('changeInfo', changeInfo, name="changeInfo"),
	path('changePw', changePw, name="changePw"),
	path('registerCancle', registerCancle, name="registerCancle"),
	path('checkDuplicate', checkDuplicateAPI, name="checkDuplicate"),
]