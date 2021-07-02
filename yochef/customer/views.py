from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import *

# Create your views here.
def signup(request):
	if str(request.user) != "AnonymousUser":
		return redirect('/')
	else:
		if request.method == "POST":
			if User.objects.filter(username=request.POST['userEmail']).exists():
				return render(request, "account_signup.html", {'error': '이메일이 중복됩니다'})
            elif Customer.objects.filter(nickname = request.POST['userNickname']).exists() :
                return render(request, "account_signup.html", {'error': '닉네임이 중복됩니다'})
            else : 
                user = User.objects.create_user(
                    username=request.POST['userEmail'], password=request.POST['password']) 
                phoneNumber = request.POST['phoneNumber']
                customer = Customer(user=user, phoneNumber=phoneNumber)
                customer.save()
                    auth.login(request, user)
		else:
			return render(request, 'account_signup.html') # html 이름 수정

def login(request):
    if str(request.user) != "AnonymousUser":
        return redirect('/')
    elif request.COOKIES.get('username') is not None:
        username = request.COOKIES.get('username')
        password = request.COOKIES.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')  
        else:
            return render(request, "account_login.html") # html 이름 수정
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.POST.get("keep_login") == "TRUE": # 자동 로그인 관련 값 재설정 필요
                response = render(request, 'home.html', {'posts': posts})
                response.set_cookie('username',username)
                response.set_cookie('password',password)
                return response
            return redirect('/')
        else:
            return  render(request, "account_login.html", {'error':'아이디나 비밀번호가 일치하지 않습니다'})
    else:
        return render(request, "account_login.html")

def logout(request):
    auth.logout(request)
    
    response = render(request, "account_login.html")
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response

def findId(request):
    return render(request, "account_findId.html")

def findPassword(request):
    return render(request, "account_findPassword.html")

def createAccount(request):
    return render(request, "account_createAccount.html")