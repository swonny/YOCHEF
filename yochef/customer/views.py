from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import *
from chef.models import *

# Create your views here.
def signup(request):
    if str(request.user) != "AnonymousUser":
        return redirect('/')
    else:
        if request.method == "POST":
            if User.objects.filter(username=request.POST['userEmail']).exists():
                return render(request, "customer_signup.html", {'error': '이메일이 중복됩니다'})
            elif request.POST['userPassword'] != request.POST['userPasswordCheck'] :
                return render(request, "customer_signup.html", {'error': '비밀번호 확인이 일치하지 않습니다'})
            else: 
                user = User.objects.create_user(
                    username=request.POST['userEmail'], password=request.POST['userPassword']) 
                phoneNumber = request.POST['userPhoneNum']
                customer = Customer(user=user, phoneNum=phoneNumber)
                customer.region = request.POST.get('region', 0)
                # regiondetail 임시 지정
                customer.regionDetail = RegionDetail.objects.get(region = 0)
                customer.name = request.POST['username']
                customer.email = user.username
                customer.phoneNum = request.POST['userPhoneNum']
                customer.save()
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request, 'customer_signup.html') # html 이름 수정

def login(request):
    if str(request.user) != "AnonymousUser":
        return redirect('/')
    elif request.COOKIES.get('userEmail') is not None:
        username = request.COOKIES.get('userEmail')
        password = request.COOKIES.get('userPassword')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')  
        else:
            return render(request, "customer_login.html") # html 이름 수정
    elif request.method == "POST":
        username = request.POST["userEmail"]
        password = request.POST["userPassword"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.POST.get("keep_login") == "TRUE": # 자동 로그인 관련 값 재설정 필요
                response = redirect('/')
                response.set_cookie('userEmail',username)
                response.set_cookie('userPassword',password)
                return response
            return redirect('/')
        else:
            return  render(request, "customer_login.html", {'error':'아이디나 비밀번호가 일치하지 않습니다'})
    else:
        return render(request, "customer_login.html")

def logout(request):
    auth.logout(request)
    response = render(request, "customer_login.html")
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response

def findId(request):
    return render(request, "customer_findId.html")

def findPw(request):
    return render(request, "customer_findPw.html")

def createAccount(request):
    return render(request, "customer_signup.html")

def apply(request): #예약하기 버튼
    schedule_id = int(request.POST['schedule'])
    schedule = Schedule.objects.get(id = schedule_id)
    course = Course.objects.get(id = int(request.POST['course']))
    book = Book()
    book.customer = request.user.customer
    book.course = course
    book.schedule = schedule
    book.personNum = int(request.POST['peopleNum'])
    book.totalPrice = schedule.post.movingPrice + (course.price * book.personNum)
    book.save()
    return render(request, 'pay_apply.html', {'course': course, 'book':book})

def payment(request): #다음 버튼
    book_id = int(request.POST['book'])
    book = Book.objects.get(id = book_id)
    coupons = HasCoupon.objects.filter(customer = request.user.customer, isUsed=False)
    book.comment = request.POST.get('comment')
    book.phoneNum = request.POST.get('phoneNum')
    book.save()
    return render(request, 'pay_payment.html', {'book':book, 'coupons' : coupons})

def payComplete(request): #결제하기 눌렀을 때
    print(request.POST['selectedCoupon'])
    print(request.POST['usingPoint'])
    print(request.POST['payment'])
    book_id = int(request.POST['book'])
    book = Book.objects.get(id = book_id)
    coupon_id = request.POST['selectedCoupon']
    if coupon_id != '':
        has_coupon = HasCoupon.objects.get(id = coupon_id)
        has_coupon.isUsed = True
        has_coupon.save()
        book.coupon = HasCoupon.objects.get(id = coupon_id)
    using_point = request.POST['usingPoint']
    if using_point != '':
        book.usedPoint = int(using_point)
        customer = request.user.customer
        customer.point = int(customer.point) - int(using_point)
        customer.save()
    payment = request.POST.get('payment')
    book.payMethod = payment
    book.save()

    # 추후 구현 된다면 실제 결제 기능까지

    return redirect('/')

# 결제 취소 기능
    #   페이지에서 버튼 기능이 구현되기 전까지 url만 넣어서 Admin 페이지에서 삭제됐는지 확인
    #   쿠폰 기록 복원
    #   포인트 기록 복원
    #   schedule 기록 복원


def registerCancle(request):
    book = Book.objects.filter(customer=request.user.customer)
    coupon_id = request.POST['selectedCoupon']
    if coupon_id != '':
        has_coupon = HasCoupon.objects.get(id = coupon_id)
        has_coupon.isUsed = False
        has_coupon.save()
        book.coupon = HasCoupon.objects.get(id = coupon_id)
    using_point = request.POST['usingPoint']
    if using_point != '':
        book.usedPoint = int(using_point)
        customer = request.user.customer
        customer.point = int(customer.point) + int(using_point)
        customer.save()
    return render(request, 'myMenu_reservation.html')



def mypage(request):
    if request.user.customer.currentVer == 0 :
        if request.method == 'GET':
            return render(request, 'mypage.html')
    else :
        if request.method == 'GET':
            profile = File.objects.get(chef = request.user.customer.chef, category = 1)
            return render(request, 'mypage.html', {'profile':profile})

    return render(request, 'mypage.html')

def mymenuLikedmenu(request):
    mylike_chefs = Like.objects.filter(customer=request.user.customer).values('chef')
    chefs_post = Post.objects.filter(chef__in = mylike_chefs)
    for chef_post in chefs_post :
        if File.objects.filter(post = chef_post, category = 4).exists():
            chef_post.cover_img = File.objects.filter(post = chef_post, category = 4)[0].attachment
    return render(request, 'myMenu_likedMenu.html', {'posts':chefs_post})

def mymenuReservation(request):
    books = Book.objects.filter(customer=request.user.customer)
    print(books)
    return render(request, 'myMenu_reservation.html', {'books': books})