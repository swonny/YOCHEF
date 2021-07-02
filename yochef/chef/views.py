from django.shortcuts import redirect, render
from .models import *

# Create your views here.

def registerChef(request, page_num=1):
    return render(request, f'registerChef_{page_num}.html')

def registerChefSubmit(request, user_id):   # 작성 중
    if page_num == '2':
        customer = request.user.Customer.objects.get(id=user_id)     # Customer() 가져오는 방법?
        chef = Chef(customer=customer)
        # profileImage = File()                             # File() 가져오는 방법?
        # profileImage = request.POST['profileImg']
        chef.nickname = request.POST['nickname']
        chef.spec = request.POST['spec']
        chef.snsLink = request.POST['snsLink']
        chef.blogLink = request.POST['blogLink']
        chef.youtubeLink = request.POST['youtubeLink']
        chef.save()
        return render(request, 'registerChef_2.html')
    elif page_num == '3': 
        customer = request.user.Customer.objects.get(id=user_id)
        chef = Chef.objects.get(customer=customer)
        post = Post(chef=chef)
        post.category = request.POST['category']
        post.region = request.POST['region']
        post.regionDetail = request.POST['regionDetail']
        post.save()
        return render(request, 'registerChef_3.html')
    elif page_num == '4':
        customer = request.user.Customer.objects.get(id=user_id)
        chef = Chef.objects.get(customer=customer)
        post = Post.objects.get(chef=chef)
        post.title = request.POST['title']
        # postCoverImage = File()
        # postCoverImage.attachment = request.POST['attachment']
        post.introduce = request.POST['introduce']
        course = Course(post=post)
        course.title = request.POST['courseTitle']
        course.price = request.POST['coursePrice']
        course.description = request.POST['courseDescribe']
        post.notice = request.POST['notice']
        post.save()
        course.save()
        return render(request, 'registerChef_4.html')
    elif page_num == '5':
        customer = request.user.Customer.objects.get(id=user_id)
        chef = Chef.objects.get(customer=customer)
        post = Post.objects.get(chef=chef)
        chef.movingPrice = request.Post['movingPrice']
        chef.save()
        return render(request, '/')

def chefSchedule(request):
    return render(request, 'chefSchedule.html')

def chefScheduleDetail(request):
    return render(request, 'chefSchedule_detail.html')