from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from chef.models import *
from .models import *
import json

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
    return render(request, 'detail.html', {'post': post})

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
    

