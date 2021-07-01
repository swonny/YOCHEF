from django.shortcuts import redirect, render
from .models import *

# Create your views here.

def registerChef(request, page_num):
    # 작성 중입니다. 
    # if page_num == '0':
    #     return
    # elif page_num == '1':
    #     chef = Chef()
    #     chef.nickname = request.GET['nickname']
    #     chef.spec = request.GET['spec']
    #     chef.snsLink = request.GET['snsLink']
    #     chef.blogLink = request.GET['blogLink']
    #     chef.youtubeLink = request.GET['youtubeLink']
    #     chef.save()
    #     return redirect(f'registerChef/{int(page_num)+1}')
    # elif page_num == '2': 
    #     return redirect(f'registerChef/{int(page_num)+1}')
    # elif page_num == '3':
    #     return
    # elif page_num == '4':
    #     return
    return render(request, f'registerChef_{page_num}.html')

def chefSchedule(request):
    return render(request, 'chefSchedule.html')