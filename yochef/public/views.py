from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from chef.models import *
from customer.models import Review
from .models import *
from datetime import date, timedelta
from django.utils.dateparse import parse_date


# Create your views here.

# 메인 페이지를 반환하는 함수
def main(request): 
    posts = Post.objects.filter(isOpen = True).order_by('registerDate')
    return render(request, 'main.html', {'posts': posts}) 

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
    schedules = Schedule.objects.filter(paymentStatus = 1).order_by('eventDate', 'id')
    return render(request, 'detail.html', {'post': post, 'courses':courses, 'reviews': reviews, 'is_review_over': is_review_over, 'schedules':schedules})

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
    posts = Post.objects.filter(isOpen=True, schedule__eventDate__range=[start_date, end_date], schedule__paymentStatus = 1, region=region)
    posts = posts.filter(Q(title__icontains = keyword) or Q(chef__nickname__icontains = keyword))
    if category:
        posts = posts.filter(category = category)
    if regionDetail < 97 :
        posts = posts.filter(regionDetail_id=regionDetail)

    # 순서 적용 잘되는지 확인 필요
    if order == 1:
        posts = posts.order_by('-registerDate')
    elif order == 2 or order == 3:
        if order == 2 : order_by = '-price'
        else : order_by = 'price'
        for post in posts :
            post.order_price = Course.objects.filter(post = post).order_by(order_by).first().price
        if order == 2:
            posts = sorted(posts, key=(lambda x: x.order_price), reverse=True)
        else :
            posts = sorted(posts, key=(lambda x: x.order_price))
    else :
        for post in posts :
            post.review_cnt = len(Review.objects.filter(post_id = post.id))
        posts = sorted(posts, key=(lambda x: x.review_cnt), reverse=True)
    for post in posts :
        if File.objects.filter(post_id = post.id, category = 3).exists():
            post.cover_img = File.objects.get(post_id = post.id, category = 3).attachment.url

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return render(request, 'postList.html', {'posts': posts, 'category': category, 'order': order, 'start_date': start_date, 'end_date': end_date, 'keyword':keyword})