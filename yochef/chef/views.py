from django.shortcuts import redirect, render
from .models import *
from public.models import *
from customer.models import *

# Create your views here.
# CRUD : Cread Read Update Delete

# registerChef_1~4.html READ & UPDATE
def registerChef(request, page_num=1):
    customer = request.user.customer
    if page_num == 1:
        if Chef.objects.filter(customer=customer).exists():
            chef = customer.chef
            if File.objects.filter(chef=chef).exists():
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
        context['profileImage'] = profileImage

        return render(request, 'registerChef_1.html', context)

    elif page_num == 2: # 1page 다음 버튼
        chef = customer.chef
        
        chef.nickname = request.POST['nickname']
        chef.spec = request.POST['spec']
        chef.snsLink = request.POST['snsLink']
        chef.blogLink = request.POST['blogLink']
        chef.youtubeLink = request.POST['youtubeLink']
        chef.save()

        if File.objects.filter(chef=chef).exists():
            profileImage = File.objects.get(chef=chef)
            profileImage.attachment = request.POST['profileImage']
        else:
            if request.POST['profileImage']:
                profileImage = File(chef=chef, category=1)
                profileImage.attachment = request.POST['profileImage']
        profileImage.save()
        
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
            postCoverImage.attachment = request.POST['coverImage']
        else:
            if request.POST['coverImage']:
                postCoverImage = File(post=post, category=4)
                postCoverImage.attachment = request.POST['coverImage']
        post.introduce = request.POST['introduce']

        # 코스 추가 : FE와 JS 활용 방식 논의 후 작성
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
        if chef.isSubmitted:
            context['message'] = "수정"
        else:
            context['message'] = "제출"

        return render(request, 'registerChef_4.html', context)

    elif page_num == 5: # 4page 제출 버튼
        chef = customer.chef

        chef.movingPrice = request.Post['movingPrice']
        chef.save()

        customer.isChef = True      # 셰프등록 승인 절차 기획 전까지 유지
        customer.save()

        return redirect('/')


# chefSchedule.html READ
def chefSchedule(request):
    chef = request.user.customer.chef
    post = Post.objects.get(chef=chef)
    schedules = Schedule.objects.filter(post=post)

    scheduleInfoList = []
    for schedule in schedules:
        book = Book.objects.get(schedule=schedule) # 코스, 인원, 총 결제 금액

        scheduleInfo = {}
        scheduleInfo['eventDate'] = schedule.eventDate
        scheduleInfo['eventTime'] = schedule.eventTime
        scheduleInfo['payment_status'] = schedule.print_payment_status
        scheduleInfo['confirm_status'] = schedule.print_confirm_status
        scheduleInfo['course'] = book.course
        scheduleInfo['personNum'] = book.personNum
        scheduleInfo['totalPrice'] = book.totalPrice
        scheduleInfo['scheduleID'] = schedule.id
        scheduleInfoList.append(scheduleInfo)

    context = {}
    context['chef'] = chef
    context['post'] = post
    context['scheduleList'] = scheduleInfoList

    return render(request, 'chefSchedule.html', context)


# chefSchedule_detail.html READ
def chefScheduleDetail(request, schedule_id):
    chef = request.user.customer.chef
    post = Post.objects.get(chef=chef)
    schedule = Schedule.objects.get(id=schedule_id)
    book = Book.objects.get(schedule=schedule)

    context = {}
    context['chef'] = chef
    context['post'] = post
    context['schedule'] = schedule
    context['book'] = book

    return render(request, 'chefSchedule_detail.html', context)


# chefSchedule_detail.html UPDATE
def scheduleConfirm(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.POST.get('scheduleConfirm'):
        schedule.confirm_status = 2
        schedule.save()
    return redirect('/chef/chefSchedule/' + str(schedule_id))


# chefSchedule_detail.html UPDATE
## 일정(예약) 승인 취소
def scheduleCancel(request, schedule_id):
    return


# editChefProfile_1.html READ
def editChefProfile(request):
    chef = request.user.customer.chef
    chefProfileImage = File.objects.get(chef=chef)

    context = {}
    context['chef'] = chef
    context['chefProfileImage'] = chefProfileImage

    return render(request, 'editChefProfile_1.html', context)


# editChefProfile_1.html UPDATE
def updateChefProfile(request, chef_id):
    chef = Chef.objects.get(id=chef_id)
    chefProfileImage = File.objects.get(chef=chef, category=1)

    chefProfileImage.attachment = request.POST.get('profileImage')
    chef.nickname = request.POST.get('nickname')
    chef.spec = request.POST.get('spec')
    chef.snsLink = request.POST.get('snsLink')
    chef.blogLink = request.POST.get('blogLink')
    chef.youtubeLink = request.POST.get('youtubeLink')

    chefProfileImage.save()
    chef.save()

    return redirect('/chef/editChefProfile/')


## 예약글 수정 페이지
# editChefProfile.html READ
def editPost(request):
    return


## 예약글 수정 내용 저장
# editChefProfile.html UPDATE
def updatePost(request):
    return