from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from public.models import *
from customer.models import *

# Create your views here.
# CRUD : Cread Read Update Delete

# registerChef_1~4.html READ & CREATE
def registerChef(request, page_num=1):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")

    customer = request.user.customer
    if page_num == 1:   # Load registerChef/1
        if Chef.objects.filter(customer=customer).exists():
            chef = customer.chef
        else:
            chef = Chef(customer=customer)
            chef.save()
        if File.objects.filter(chef=chef, category=1).exists():
            profileImage = File.objects.get(chef=chef, category=1)
        else:
            profileImage = File(chef=chef, attachment="/static/image/more.png", category=1)
            profileImage.save()
        if File.objects.filter(chef=chef, category=2).exists():
            chef.specImages = File.objects.filter(chef=chef, category=2)
        else:
            pass
        if Post.objects.filter(chef=chef).exists():
            post = chef.post
        else:
            post = Post(chef=chef)
            post.save()
        context = {
            "customer" : customer,
            "chef" : chef,
            "profileImage" : profileImage,
        }
        return render(request, 'registerChef_1.html', context)

    elif page_num == 2: # save registerChef/1, load registerChef/2
        chef = customer.chef
        post = chef.post
        if request.method == "POST":
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
            if request.FILES.getlist('specImage'):
                File.objects.filter(chef=chef, category=2).delete()
                specImages = request.FILES.getlist('specImage')
                for index, image in enumerate(specImages):
                    File.objects.create(attachment=image, chef=chef, category=2, order=index+1)
        context = {
            "customer" : customer,
            "chef" : chef,
            "post" : post,
        }
        return render(request, 'registerChef_2.html', context)

    elif page_num == 3: # save registerChef/2, load registerChef/3
        chef = customer.chef
        post = chef.post
        if request.method == "POST":
            post.category = request.POST.get('category')
            post.region = request.POST.get('residence')
            post.regionDetail = RegionDetail.objects.get(id=request.POST.get('residenceDetail'))
            post.save()
        if File.objects.filter(post=post, category=4).exists():
            postCoverImage = File.objects.get(post=post, category=4)
        else:
            postCoverImage = None
        courses = Course.objects.filter(post=post)
        for course in courses:
            course.images = File.objects.filter(course=course, category=3)
        context = {
            "chef" : chef,
            "post" : post,
            "postCoverImage" : postCoverImage,
            "courses" : courses,
        }
        return render(request, 'registerChef_3.html', context)

    elif page_num == 4: # save registerChef/3, load registerChef/4
        chef = customer.chef
        post = chef.post
        if request.method == "POST":
            post.title = request.POST.get('title')
            if request.FILES.get('postCoverInput'):  # 직접 수정이 불가능하니 기존에 입력된 DB 삭제 후 재입력
                postCoverImage = request.FILES.get('postCoverInput')
                File.objects.filter(post=post, category=4).delete()              
                File.objects.create(post=post, attachment=postCoverImage, category=4)
            post.introduce = request.POST.get('introduce')
            post.notice = request.POST.get('notice')
            post.save()
            courseCount = request.POST.get("courseCount")
            for i in range(1, int(courseCount)+1):
                if Course.objects.filter(post=post, order=i).exists():
                    course = Course.objects.get(post=post, order=i)
                else:
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
        context = {
            "chef" : chef,
            "post" : post,
            "courses" : Course.objects.filter(post=post)
        }
        return render(request, 'registerChef_4.html', context)

    elif page_num == 5: # save registerChef/4
        chef = customer.chef
        post = chef.post
        if request.method == "POST":
            post.movingPrice = request.POST.get('movingPriceInput')
            chef.isSubmitted = True
            customer.isChef = True      # 셰프등록 승인 절차 기획 전까지 유지
            customer.currentVer = 1
            post.save()
            chef.save()
            customer.save()
        return redirect('chefSchedule')


# editChefProfile_1.html READ
def editChefProfile(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    chef = request.user.customer.chef
    profileImage = File.objects.get(chef=chef, category=1)
    if File.objects.filter(chef=chef, category=2).exists():
        chef.specImages = File.objects.filter(chef=chef, category=2)
    context = {
        "chef" : chef,
        "profileImage" : profileImage
    }
    return render(request, 'editChefProfile_1.html', context)


# editChefProfile_1.html UPDATE
def updateChefProfile(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    chef = request.user.customer.chef
    if request.method == "POST":
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
        if request.FILES.getlist('specImage'):
            File.objects.filter(chef=chef, category=2).delete()
            specImages = request.FILES.getlist('specImage')
            for index, image in enumerate(specImages):
                File.objects.create(attachment=image, chef=chef, category=2, order=index+1)
    return redirect('editChefProfile')


# editChefProfile_2.html READ
def editPost(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    chef = request.user.customer.chef
    post = chef.post
    if File.objects.filter(post=post, category=4).exists():
        postCoverImage = File.objects.get(post=post, category=4)
    else:
        postCoverImage = None
    courses = Course.objects.filter(post=post)
    for course in courses:
        course.images = File.objects.filter(course=course, category=3)
    context = {
        "chef" : chef,
        "post" : post,
        "postCoverImage" : postCoverImage,
        "courses" : courses,
    }
    return render(request, 'editChefProfile_2.html', context)


# editChefProfile_2.html CREATE
def updatePost(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    post = request.user.customer.chef.post
    if request.method == "POST":
        post.category = request.POST.get('category')
        post.region = request.POST.get('residence')
        post.regionDetail = RegionDetail.objects.get(id=request.POST.get('residenceDetail'))
        post.title = request.POST.get('title')
        if request.FILES.get('postCoverInput'):  # 직접 수정이 불가능하니 기존에 입력된 DB 삭제 후 재입력
            postCoverImage = request.FILES.get('postCoverInput')
            File.objects.filter(post=post, category=4).delete()              
            File.objects.create(post=post, attachment=postCoverImage, category=4)
        post.introduce = request.POST.get('introduce')
        post.notice = request.POST.get('notice')
        post.save()
        #courseCount = request.POST.get("courseCount") if request.POST.get("courseCount") else 0
        courseCount = request.POST.get("courseCount")
        for i in range(1, int(courseCount)+1):
                if Course.objects.filter(post=post, order=i).exists():
                    course = Course.objects.get(post=post, order=i)
                else:
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
    return redirect('editPost')


# editChefProfile_3.html READ
def editMovingPrice(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    post = request.user.customer.chef.post
    courses = Course.objects.filter(post=post)
    context = {
        "post" : post,
        "courses" : courses
    }
    return render(request, 'editChefProfile_3.html', context)


# editChefProfile_3.html UPDATE
def updateMovingPrice(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    post = request.user.customer.chef.post
    if request.method == "POST":
        post.movingPrice = request.POST.get('movingPriceInput')
        post.save()
    return redirect('editMovingPrice')


# chefSchedule.html READ
def chefSchedule(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    chef = request.user.customer.chef
    post = chef.post
    schedules = Schedule.objects.filter(post=post).order_by('-eventDate')
    scheduleInfoList = []
    for schedule in schedules:
        if Book.objects.filter(schedule=schedule, paymentStatus=2).exists():  # 코스, 인원, 총 결제 금액
            books = Book.objects.filter(schedule=schedule, paymentStatus__gt=1)
            for book in books: 
                scheduleInfo = {}
                scheduleInfo['scheduleID'] = schedule.id
                scheduleInfo['region'] = schedule.region
                scheduleInfo['regionDetail'] = schedule.regionDetail
                scheduleInfo['eventDate'] = schedule.eventDate
                scheduleInfo['eventTime'] = schedule.eventTime
                scheduleInfo['confirmStatus'] = schedule.print_confirmStatus
                scheduleInfo['bookID'] = book.id
                scheduleInfo['course'] = book.course
                scheduleInfo['personNum'] = book.personNum
                scheduleInfo['totalPrice'] = book.totalPrice
                scheduleInfo['paymentStatus'] = book.print_paymentStatus
                scheduleInfoList.append(scheduleInfo)
        else:
            scheduleInfo = {}
            scheduleInfo['region'] = schedule.region
            scheduleInfo['regionDetail'] = schedule.regionDetail
            scheduleInfo['eventDate'] = schedule.eventDate
            scheduleInfo['eventTime'] = schedule.eventTime
            scheduleInfo['confirmStatus'] = schedule.print_confirmStatus
            scheduleInfo['scheduleID'] = schedule.id
            scheduleInfoList.append(scheduleInfo)
    context = {
        "chef" : chef,
        "post" : post,
        "scheduleList" : scheduleInfoList,
    }
    return render(request, 'chefSchedule.html', context)


# chefSchedule.html CREATE
def addSchedule(request):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    post = request.user.customer.chef.post
    if request.method == "POST":
        schedule = Schedule(post=post)
        schedule.region = request.POST.get("residence")
        schedule.regionDetail = RegionDetail.objects.get(id=request.POST.get("residenceDetail"))
        schedule.eventDate = request.POST.get("scheduleDate")
        schedule.eventTime = request.POST.get("scheduleTime")
        schedule.save()
    return redirect("chefSchedule")


# chefSchedule.html DELETE
def deleteSchedule(request):
    schedule_id = request.POST['scheduleID']
    schedule = Schedule.objects.get(id=schedule_id)
    if Book.objects.filter(schedule=schedule, paymentStatus__in=[2,3]).exists():
        return JsonResponse({}, status=403)
    else:
        Schedule.objects.filter(id=schedule_id).delete()
        return JsonResponse({}, status=200)


# chefSchedule_detail.html READ
def chefScheduleDetail(request, book_id):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    chef = request.user.customer.chef
    post = chef.post
    book = Book.objects.get(id=book_id)
    schedule = book.schedule
    context = {
        "chef" : chef,
        "post" : post,
        "schedule" : schedule,
        "book" : book,
    }
    return render(request, 'chefSchedule_detail.html', context)


# chefSchedule_detail.html UPDATE 1
def scheduleConfirm(request, book_id):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    if request.method == "POST":
        book = Book.objects.get(id=book_id)
        schedule = book.schedule
        if request.POST.get('scheduleConfirm'):
            schedule.confirmStatus = 2	# 1: 승인대기  2: 승인됨  3. 취소됨
            schedule.save()
    return redirect('chefScheduleDetail', book_id)


# chefSchedule_detail.html UPDATE
def scheduleCancel(request, book_id):
    if str(request.user) == "AnonymousUser":
        return redirect("/customer/login")
    elif request.user.customer.isChef == False:
        return redirect("/chef/registerChef/1")
    if request.method == "POST":
        book = Book.objects.get(id=book_id)
        schedule = book.schedule
        if request.POST.get('scheduleCancel'):
            schedule.confirmStatus = 3	# 0: 결제대기  1: 승인대기  2: 승인완료  3: 승인취소
            book.paymentStatus = 3 # 1: 결제대기  2: 결제완료  3: 결제취소
            schedule.save()
            book.save()
    return redirect('chefScheduleDetail', book_id)