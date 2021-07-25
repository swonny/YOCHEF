from django.shortcuts import redirect, render
from .models import *
from public.models import *
from customer.models import *

# Create your views here.
# CRUD : Cread Read Update Delete

# registerChef_1~4.html READ & UPDATE
def registerChef(request, page_num=1):
    customer = request.user.customer
    if page_num == 1:   # Load registerchef/1
        if Chef.objects.filter(customer=customer).exists():
            chef = customer.chef
        else:
            chef = Chef(customer=customer)
            chef.save()

        if File.objects.filter(chef=chef).first().attachment:
            profileImage = File.objects.get(chef=chef, category=1)
        else:
            profileImage = File(chef=chef, attachment="../media/media/default_chef_profile_image.png", category=1)
            profileImage.save()

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

    elif page_num == 2: # save registerchef/1, load registerchef/2
        chef = customer.chef
        post = Post.objects.get(chef=chef)
        
        chef.nickname = request.POST.get('nickname')
        chef.spec = request.POST.get('spec')
        chef.snsLink = request.POST.get('snsLink')
        chef.blogLink = request.POST.get('blogLink')
        chef.youtubeLink = request.POST.get('youtubeLink')
        chef.save()

        if request.FILES.get('profileImage'):
            profileImage = File.objects.get(chef=chef, category=1)
            profileImage.attachment = request.FILES.get('profileImage')
            profileImage.save()
        
        context = {}
        context['customer'] = customer
        context['chef'] = chef
        context['post'] = post

        return render(request, 'registerChef_2.html', context)

    elif page_num == 3: # save registerchef/2, load registerchef/3
        chef = customer.chef
        post = Post.objects.get(chef=chef)

        post.category = request.POST.get('category')
        post.region = request.POST.get('region')
        post.regionDetail = request.POST.get('regionDetail')
        post.save()

        if File.objects.filter(post=post, category=4).exists():
            postCoverImage = File.objects.get(post=post, category=4)
        else:
            postCoverImage = None

        courses = Course.objects.filter(post=post)
        for course in courses:
            course.images = File.objects.filter(course=course, category=3)

        context = {}
        context['chef'] = chef
        context['post'] = post
        context['postCoverImage'] = postCoverImage
        context['courses'] = courses

        return render(request, 'registerChef_3.html', context)

    elif page_num == 4: # save registerchef/3, load registerchef/4
        chef = customer.chef
        post = chef.post

        post.title = request.POST.get('title')

        if request.FILES.get('postCoverInput'):  # list로 받아옴 / 직접 수정이 불가능하니 기존에 입력된 DB 삭제 후 재입력
            postCoverImage = request.FILES.get('postCoverInput')
            File.objects.filter(post=post, category=4).delete()              
            File.objects.create(post=post, attachment=postCoverImage, category=4)

        post.introduce = request.POST.get('introduce')

        Course.objects.filter(post=post).delete()
        courseCount = request.POST.get("courseCount")
        for i in range(1, int(courseCount)+1):
            course = Course(post=post, order=i)
            course.title = request.POST.get("courseTitle"+str(i))
            course.price = request.POST.get("coursePrice"+str(i))
            course.description = request.POST.get("courseDescribe"+str(i))
            course.save()

            if request.FILES.getlist("courseImg"+str(i)+"[]"):
                courseImageFiles = request.FILES.getlist("courseImg"+str(i)+"[]")
                File.objects.filter(course=course, category=3).delete() # 직접 수정이 불가능하니 기존에 입력된 DB 삭제 후 재입력
                for index, file in enumerate(courseImageFiles):
                    File.objects.create(attachment=file, course=course, category=3, order=index+1)     

        post.notice = request.POST.get('notice')
        post.save()
        
        context = {}
        context['chef'] = chef
        context['post'] = post
        context['courses'] = Course.objects.filter(post=post)

        return render(request, 'registerChef_4.html', context)

    elif page_num == 5: # save registerchef/4
        chef = customer.chef

        chef.movingPrice = request.POST.get('movingPrice')
        chef.isSubmitted = True
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
        scheduleInfo['confirmStatus'] = schedule.print_confirmStatus
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


# chefSchedule.html UPDATE ADD
def addSchedule(request):
    chef = request.user.customer.chef
    post = chef.post

    newSchedule = Schedule(post=post)
    newSchedule.eventDate = request.POST.get("scheduleDate")
    newSchedule.eventTime = request.POST.get("scheduleTime")
    newSchedule.confirmStatus = 1
    newSchedule.save()

    return redirect("update/")


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


# chefSchedule_detail.html UPDATE 1
def scheduleConfirm(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.POST.get('scheduleConfirm'):
        schedule.confirmStatus = 2	# 1: 승인대기  2: 승인됨  3. 취소됨
        schedule.save()
    return redirect('/chef/chefSchedule/' + str(schedule_id))


# chefSchedule_detail.html UPDATE
def scheduleCancel(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    book = Book.objects.get(schedule=schedule)
    if request.POST.get('scheduleCancel'):
        schedule.confirmStatus = 3	# 1: 승인대기  2: 승인됨  3. 취소됨
        book.paymentStatus = 3 # 1:결제대기 2:결제완료 3:결제취소s
        schedule.save()
        book.save()
    return redirect('/chef/chefSchedule/' + str(schedule_id))


# editChefProfile_1.html READ
def editChefProfile(request):
    chef = request.user.customer.chef
    profileImage = File.objects.get(chef=chef, category=1)

    context = {}
    context['chef'] = chef
    context['profileImage'] = profileImage

    return render(request, 'editChefProfile_1.html', context)


# editChefProfile_1.html UPDATE
def updateChefProfile(request):
    chef = request.user.customer.chef
    
    if request.FILES.get('profileImage'):
        profileImage = File.objects.get(chef=chef, category=1)
        profileImage.attachment = request.FILES.get('profileImage')
        profileImage.save()
        
    chef.nickname = request.POST.get('nickname')
    chef.spec = request.POST.get('spec')
    chef.snsLink = request.POST.get('snsLink')
    chef.blogLink = request.POST.get('blogLink')
    chef.youtubeLink = request.POST.get('youtubeLink')
    chef.save()

    return redirect('/chef/editChefProfile/')


# editChefProfile_2.html READ
def editPost(request):
    chef = request.user.customer.chef
    post = Post.objects.get(chef=chef)
    coverImages = File.objects.filter(post=post, category=4)
    courses = Course.objects.filter(post=post)
    courseImageList = []
    for course in courses:
        courseImages = File.objects.filter(course=course, category=3)
        courseImageList.append(courseImages)
    region = post.region
    regionDetail = post.regionDetail

    context = {}
    context['chef'] = chef
    context['post'] = post
    context['coverImages'] = coverImages
    context['courses'] = courses
    context['courseImageList'] = courseImageList
    context['region'] = region
    context['regionDetail'] = regionDetail

    return render(request, 'editChefProfile_2.html', context)


# editChefProfile_2.html UPDATE
def updatePost(request):
    post = request.user.customer.chef.post
    coverImages = File.objects.filter(post, category=4)
    courses = Course.objects.filter(post=post)

    post.category = request.POST('category')
    post.region = request.POST('region')
    post.regionDetail = request.POST.get('regionDetail')
    post.title = request.POST.get('title')
    post.intoruce = request.POST.get('introduce')
    post.notice = request.POST.get('notice')

    # 파일 여러 개 입력 받는 방법?
    # coverImages1.attachment = request.POST.get['coverImage']
    # coverImages2.attachment = request.POST.get['coverImage']
    # coverImages3.attachment = request.POST.get['coverImage']
    
    # 코스 수정사항 입력 받는 방법?
    # course1
    # course2
    # course3

    post.save()
    for coverImage in coverImages:
        coverImage.save()
    for course in courses:
        course.save()

    return redirect('/chef/editPost/')


# editChefProfile_3.html READ
def editMovingPrice(request):
    post = request.user.customer.chef.post
    courses = Course.objects.filter(post=post)

    context = {}
    context['post'] = post
    context['courses'] = courses

    return render(request, 'editChefProfile_3.html', context)


# editChefProfile_3.html UPDATE
def updateMovingPrice(request):
    post = request.user.customer.chef.post
    post.movingPrice = request.POST.get['movingPrice']
    post.save()
    return redirect('/chef/editMovingPrice/')