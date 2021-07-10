from django.shortcuts import redirect, render
from .models import *
from public.models import *

# Create your views here.

def registerChef(request, page_num=1):
    customer = request.user.customer
    if page_num == 1:
        if Chef.objects.filter(customer=customer).exists():
            chef = customer.chef
            profileImage = File.objects.get(chef=chef)
        else:
            chef = Chef(customer=customer)
            profileImage = File(chef=chef, category=1)
            chef.save()
        if Post.objects.filter(chef=chef).exists():
            post = chef.post
        else:
            post = Post(chef=chef)
            post.save()

        context = {}
        context['customer'] = customer
        context['chef'] = chef

        return render(request, 'registerChef_1.html', context)

    elif page_num == 2: # 1page 다음 버튼
        chef = customer.chef
        profileImage = File.objects.get(chef=chef)

        chef.nickname = request.POST['nickname']
        chef.spec = request.POST['spec']
        chef.snsLink = request.POST['snsLink']
        chef.blogLink = request.POST['blogLink']
        chef.youtubeLink = request.POST['youtubeLink']
        chef.save()
        # profileImage.attachment = request.POST['profileImage']
        # profileImage.save()
        customer.isChef = True
        customer.save()

        context = {}
        context['customer'] = customer
        context['chef'] = chef
        context['profileImage'] = profileImage

        return render(request, 'registerChef_2.html', context)

    elif page_num == 3: # 2page 다음 버튼
        chef = customer.chef
        post = chef.post
        post.category = request.POST['category']
        post.region = request.POST['region']
        post.regionDetail = request.POST['regionDetail']
        post.save()

        context = {}
        context['chef'] = chef
        context['post'] = post

        return render(request, 'registerChef_3.html', context)

    elif page_num == 4: # 3page 다음 버튼
        chef = customer.chef
        post = chef.post
        post.title = request.POST['title']
        if File.objects.filter(post=post).exists():
            postCoverImage = File.objects.get(post=post)
        else:
            postCoverImage = File(post=post)
        postCoverImage.attachment = request.POST['coverImage']
        post.introduce = request.POST['introduce']

        # FE와 JS 활용 방식 논의 후 작성
        #if Course.objects.filter(post=post).exists():   
        #    course = Course.objects.filter(post=post).first()
        #else:
        course = Course(post=post)
        course.title = request.POST['courseTitle']
        course.price = request.POST['coursePrice']
        course.description = request.POST['courseDescribe']

        post.notice = request.POST['notice']
        post.save()
        course.save()

        context = {}
        context['chef'] = chef
        context['post'] = post

        return render(request, 'registerChef_4.html')

    elif page_num == 5: # 4page 제출 버튼
        chef = customer.chef
        post = chef.post
        chef.movingPrice = request.Post['movingPrice']
        chef.save()
        return redirect('/')


def chefSchedule(request):
    return render(request, 'chefSchedule.html')


def chefScheduleDetail(request):
    return render(request, 'chefSchedule_detail.html')