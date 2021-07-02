from django.urls import path
from .views import *
urlpatterns = [
	path('login', login, name='login'),
	path('logout', logout, name='logout'),
	path('signup', signup, name='signup'),
	path('findId', findId, name='findId'),
	path('findPassword', findPassword, name='findPassword'),
	path('createAccount', createAccount, name='createAccount'),
	path('apply', apply, name='apply'),
	path('payment', payment, name='payment'),
]