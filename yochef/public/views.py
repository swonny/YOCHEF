from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from chef.models import *
from customer.models import Coupon, Customer, HasCoupon, Review, Book
from .models import *
from datetime import date, timedelta
from django.utils.dateparse import parse_date


# Create your views here.

# 메인 페이지를 반환하는 함수
def main(request): 
    posts = Post.objects.filter(isOpen = True).order_by('-registerDate')
    schedules = Schedule.objects.filter(post__in = posts)
    # paymentStatus 관련 필터
    available_posts_id = []
    for schedule in schedules :
        if Book.objects.filter(schedule = schedule, paymentStatus = 2).exists() :
            continue
        else: 
            if schedule.post.id not in available_posts_id :
                available_posts_id.append(schedule.post.id)
    posts = posts.filter(id__in = available_posts_id)
    
    buffet_posts = posts.filter(category = 1)[:5]
    korean_posts = posts.filter(category = 2)[:5]
    japanese_posts = posts.filter(category = 3)[:5]
    
    return render(request, 'main.html', {'buffet_posts': buffet_posts, 'korean_posts': korean_posts, 'japanese_posts':japanese_posts}) 

# 현재 유저의 사용 버전을 변경하는 함수
def changePageVer(request):
    if request.user.customer.currentVer == 1:
        request.user.customer.currentVer = 0
    else : 
        request.user.customer.currentVer = 1
    request.user.customer.save()
    return redirect('/')

# 예약글 상세 페이지를 반환해주는 함수
def detail(request, post_id):
    post = Post.objects.get(id = post_id)
    courses = Course.objects.filter(post = post)
    reviews = Review.objects.filter(post = post)
    is_review_over = False
    if len(reviews) > 4 : is_review_over = True
    reviews = reviews[:4]
    # 회원 이미지 논의 필요 - 수정 필요
    schedules = Schedule.objects.all().order_by('eventDate', 'id')
    try:
        post_cover_imgurl = File.objects.get(post=post, category=4).attachment.url
    except:
        post_cover_imgurl = None
    post_imgs = File.objects.filter(post=post, category=3).order_by('order')
    if post_imgs.count() < 3 :
        more_img = 1
    else :
        more_img = post_imgs[2]
    try:
        profile_imgurl = File.objects.get(chef=request.user.customer.chef, category=1).attachment.url
    except:
        profile_imgurl = None

    for course in courses:
        course.course_imgs = File.objects.filter(course=course, category=3)

    # book - paymentStatus 관련 필터 추가
    available_schedules = []
    for schedule in schedules :
        if not Book.objects.filter(schedule = schedule, paymentStatus = 2).exists() : 
            available_schedules.append(schedule)
    
    #postLike 유무
    print(request.user)
    if not request.user.is_authenticated :
        is_like = False
    elif Like.objects.filter(customer=request.user.customer, chef=post.chef).exists():
        is_like = True
    else: 
        is_like = False
    
    return render(request, 'detail.html', {'post': post, 'courses':courses, 'reviews': reviews, 'is_review_over': is_review_over, 'schedules':available_schedules
    , 'post_cover_imgurl': post_cover_imgurl, 'post_imgs_uptotwo': post_imgs[:2], 'more_img': more_img, 'post_imgs': post_imgs,
    'profile_imgurl':profile_imgurl, 'is_like': is_like})

def reviewDetail(request, post_id):
    reviews = Review.objects.filter(post_id=post_id)
    return render(request, 'reviewDetail.html', {'reviews': reviews})

# 지역을 반환해주는 함수
def getRegionAPI(request):
    return JsonResponse({1:"서울", 2:"경기", 3:"인천", 4:"부산", 5:"경상·대구·울산", 6:"대전·충청", 7:"강원", 8:"광주·전라·제주"}, status=200)

# 세부 지역을 반환해주는 함수
def getRegionDetailAPI(request):
    region = int(request.POST['region_id'])
    region_all = list(RegionDetail.objects.filter(id__lte = 104, id__gte = 97, region = region).values('id', 'detailName'))
    region_details = region_all + list(RegionDetail.objects.filter(region = region, id__lt = 97).values('id', 'detailName'))
    return JsonResponse({'region_details':region_details}, status=200)

def changeFile(request):
    fileValue = request.POST.get('profileImg', None)
    id = request.POST.get('id', 0)
    attachment = File()
    if id != "":
        attachment = File.objects.get(id=int(id))
    else:
        category = int(request.POST['category'])
        attachment.category = category
        if category == 1:
            attachment.chef = request.user.customer.chef
    attachment.attachment = fileValue
    attachment.save()
    return redirect(request.POST['url'])
    
def postList(request, category=0, order=0):
    category = int(request.GET.get('category', 0))
    if category == 0:
        category = int(request.POST.get('category', 0))
    order = int(request.POST.get('order', 0))
    start_date = request.POST.get('startDate', "")
    end_date = request.POST.get('endDate', "")
    region = int(request.POST.get('residence', 0))
    regionDetail = int(request.POST.get('residenceDetail', 97))
    keyword = request.POST.get('keyword', "")
    if start_date == "" : start_date = date.today()
    else: start_date = parse_date(start_date)
    if end_date == "" : end_date = date.today()+timedelta(days=7)
    else: end_date = parse_date(end_date)
    posts = Post.objects.filter(isOpen=True, schedule__eventDate__range=[start_date, end_date], region=region)
    schedules = Schedule.objects.filter(post__in = posts)
    posts = posts.filter(Q(title__icontains = keyword) or Q(chef__nickname__icontains = keyword))
    if category:
        posts = posts.filter(category = category)
    if regionDetail < 97 :
        posts = posts.filter(regionDetail_id=regionDetail)

    # 순서 적용 잘되는지 확인 필요
    if order == 1:
        posts = posts.order_by('-registerDate')

    # paymentStatus 관련 필터
    available_posts = []
    for schedule in schedules :
        if Book.objects.filter(schedule = schedule, paymentStatus = 2).exists() :
            continue
        else: 
            if schedule.post not in available_posts :
                available_posts.append(schedule.post)
    
    if order == 2 or order == 3:
        if order == 2 : order_by = '-price'
        else : order_by = 'price'
        for post in available_posts :
            post.order_price = Course.objects.filter(post = post).order_by(order_by).first().price
        if order == 2:
            posts = sorted(available_posts, key=(lambda x: x.order_price), reverse=True)
        else :
            posts = sorted(available_posts, key=(lambda x: x.order_price))
    elif order == 4 :
        for post in available_posts :
            post.review_cnt = len(Review.objects.filter(post_id = post.id))
        posts = sorted(available_posts, key=(lambda x: x.review_cnt), reverse=True)
    
    for post in available_posts :
        if File.objects.filter(post_id = post.id, category = 3).exists():
            post.cover_img = File.objects.get(post_id = post.id, category = 3).attachment.url

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return render(request, 'postList.html', {'posts': available_posts, 'category': category, 'order': order, 'start_date': start_date, 'end_date': end_date, 'keyword':keyword})


def postLikeAPI(request):
    status = int(request.POST['status'])
    post_id = int(request.POST['postId'])
    chef = Post.objects.get(id=post_id).chef
    if status :
        like = Like()
        like.customer = request.user.customer
        like.chef = chef
        like.save()
    else :
        Like.objects.filter(customer=request.user.customer, chef=chef).delete()
    return JsonResponse({}, status=200)

def getCouponAPI(request):
    coupons = list(HasCoupon.objects.filter(customer = request.user.customer).values('id', 'coupon__title', 'coupon__description', 'coupon__validDate',  'coupon__offrate', 'isUsed'))
    return JsonResponse({'coupons': coupons}, status= 200)

