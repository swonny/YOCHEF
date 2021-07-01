from django.shortcuts import redirect, render
from .models import *

# Create your views here.

def registerChef(request, page_num, chef=None, post=None):
    if page_num == '0':
        return render(request, 'registerChef_1.html')
    # elif page_num == '1':
    #     chef = Chef()
    #     # profileImage = File()
    #     # profileImage = request.GET['profileImg']  # profileImage
    #     chef.nickname = request.GET['nickname']
    #     chef.spec = request.GET['spec']
    #     chef.snsLink = request.GET['snsLink']
    #     chef.blogLink = request.GET['blogLink']
    #     chef.youtubeLink = request.GET['youtubeLink']
    #     chef.save()
    #     return render(request, 'registerChef_2.html', {'chef': chef})
    # elif page_num == '2': 
    #     post = Post()
    #     post.category = request.GET['category']
    #     post.region = request.GET['region']
    #     post.regionDetail = request.GET['regionDetail']
    #     post.save()
    #     return render(request, 'registerChef_3.html', {'post': post})
    # elif page_num == '3':
    #     post.title = request.GET['title']
    #     # postCoverImage = File()
    #     # postCoverImage.attachment = request.GET['attachment']
    #     post.introduce = request.GET['introduce']
    #     post.spec = request.GET['spec']
    elif page_num == '4':
        return render(request, '/')
    return render(request, f'registerChef_{int(page_num)+1}.html')

def chefSchedule(request):
    return render(request, 'chefSchedule.html')