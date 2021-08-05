from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import *
from chef.models import *
from django.contrib.auth.hashers import check_password
import requests     # For KakaoPay API

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

# 제우스 카카오페이 작업 시작
def kakaoPayLogic(request):
    #postTitle = request.POST['postTitle']
    #personNum = request.POST['personNum']
    #totalPrice = request.POST['totalPrice']
    #vat = int(totalPrice) / 11
    #tax_free = int(totalPrice) - vat
    _admin_key = '43e1846e5c8f2fb293d6460e124d4a93'
    _url = f"https://kapi.kakao.com/v1/payment/ready"
    _headers = {
        'Authorization' : f"KakaoAK {_admin_key}",
    }
    _data = {
        'cid' : 'TC0ONETIME',
        'partner_order_id' : 'partner_order_id',
        'partner_user_id': f'partner_user_id',
        'item_name' : f'[Yochef]',
        'quantity' : f'1',
        'total_amount' : f'10000',
        'vat_amount' : f'0',
        'tax_free_amount' : f'0',
        'approval_url' : 'http://127.0.0.1:8000/customer/paySuccess',
        'fail_url' : 'http://127.0.0.1:8000/customer/payFail',
        'cancel_url' : 'http://127.0.0.1:8000/customer/payCancel',
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    print("_result 출력 : ", _result)
    request.session['tid'] = _result['tid']
    return redirect(_result['next_redirect_pc_url'])

def paySuccess(request):
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = '43e1846e5c8f2fb293d6460e124d4a93' # 입력필요
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    if _result.get('msg'):
        print(_result.get('msg'))
        return redirect('/customer/payFail')
    else:
        # * 사용하는 프레임워크별 코드를 수정하여 배포하는 방법도 있지만
        #   Req Header를 통해 분기하는 것을 추천
        print(_result)
        return render(request, 'pay_success.html')

def payFail(request):
    return render(request, 'pay_fail.html')

def payCancel(request):
    return render(request, 'pay_cancel.html')
# 제우스 카카오페이 작업 끝

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
    # 마이페이지 셰프랑 손님 구분 없음
    if request.user.customer.currentVer == 0 :
        return render(request, 'mypage.html')
    else :
        if request.method == 'GET':
            profile = File.objects.get(chef = request.user.customer.chef, category = 1)
            return render(request, 'mypage.html', {'profile':profile})
    return render(request, 'mypage.html')



def changeInfo(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    customer = request.user.customer
    customer.name = request.POST.get('nickname')
    customer.phoneNum = request.POST.get('phoneNum')
    customer.save()
    return redirect('/customer/mypage')



def changePw(request):
    if request.method == "POST":
        currentUserPw = request.POST.get("currentUserPw")
        user = request.user
        if check_password(currentUserPw,user.password):
            new_password = request.POST.get("userPw")
            password_confirm = request.POST.get("userPwCheck")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect('/customer/mypage')
    return render(request, "mypage.html")




def mymenuLikedmenu(request):
    mylike_chefs = Like.objects.filter(customer=request.user.customer).values('chef')
    chefs_post = Post.objects.filter(chef__in = mylike_chefs)
    for chef_post in chefs_post :
        if File.objects.filter(post = chef_post, category = 4).exists():
            chef_post.cover_img = File.objects.filter(post = chef_post, category = 4)[0].attachment
    return render(request, 'myMenu_likedMenu.html', {'posts':chefs_post})

def mymenuReservation(request):
    books = Book.objects.filter(customer=request.user.customer)
    return render(request, 'myMenu_reservation.html', {'books': books})

def checkDuplicateAPI(request):
    ok = True
    if User.objects.filter(username = request.POST['email']).exists() :
        ok = False
    print(request.POST['email'])
    return JsonResponse({'ok': ok}, status=200)