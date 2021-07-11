from django.shortcuts import redirect, render
from .models import *
from public.models import *
from customer.models import *

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
        context['profileImage'] = profileImage

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
        profileImage.attachment = request.POST['profileImage']
        profileImage.save()
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
        post = chef.post
        chef.movingPrice = request.Post['movingPrice']
        chef.save()

        return redirect('/')


def chefSchedule(request):
    chef = request.user.customer.chef
    post = Post.objects.get(chef=chef)
    schedules = Schedule.objects.filter(post=post)
    course = Course.objects.filter(post=post).first()

    scheduleInfoList = []
    amount, course_list, totalPrice = 0, [], 0
    for schedule in schedules:
        scheduleInfo = {}
        scheduleInfo['registerDate'] = schedule.startTime
        scheduleInfo['status'] = schedule.status

        books = Book.objects.filter(schedule=schedule) # 코스, 인원, 총 결제 금액
        course_list = []
        for book in books:
            totalPrice += book.totalPrice

            bookDetails = BookDetail.objects.filter(book=book)
            for bookdetail in bookDetails:
                course_list.append(bookdetail.course.title)
                amount += bookdetail.amount

        scheduleInfo['course'] = list(set(course_list))
        scheduleInfo['amount'] = amount
        scheduleInfo['totalPrice'] = totalPrice
        scheduleInfo['scheduleID'] = schedule.id
        
        scheduleInfoList.append(scheduleInfo)
        amount, course_list, totalPrice = 0, [], 0

    # """ 기획 case1: 기존 방식 """
    # amount, course, totalPrice = 0, [], 0
    # registerDates, statuses, courses, amounts, totalPrices, scheduleIds = [[] for _ in range(6)]
    # for schedule in schedules:
    #     #registerDates.append(schedule.eventDate)    # 예약 날짜
    #     registerDates.append(schedule.startTime)
    #     statuses.append(schedule.status)            # 예약 현황

    #     books = Book.objects.filter(schedule=schedule) # 코스, 인원, 총 결제 금액
    #     for book in books:
    #         bookDetails = BookDetail.objects.filter(book=book)
    #         for bookdetail in bookDetails:
    #             course.append(bookdetail.course.title)
    #             amount += bookdetail.amount
    #         totalPrice += book.totalPrice

    #     course = list(set(course)) # 중복 내용 제거
    #     courses.append(course)
    #     amounts.append(amount)
    #     totalPrices.append(totalPrice)
    #     amount, course, totalPrice = 0, [], 0 # 초기화
    #     # 상세 내역용 일정id
    #     scheduleIds.append(schedule.id)

    # """ 기획 case2: bookDetail 모델 대신, Book 모델이 course, amount 필드를 포함한 경우 """
    # amount, course, totalPrice = 0, [], 0
    # registerDates, statuses, courses, amounts, totalPrices, scheduleIds = [[] for _ in range(6)]
    # for schedule in schedules:
    #     registerDates.append(schedule.eventDate)
    #     statuses.append(schedule.status)
    #     books = Book.objects.filter(schedule=schedule)
    #     for book in books:
    #         course.append(book.course)
    #         amount += book.amount
    #         totalPrice += book.totalPrice

    #     course = list(set(course))
    #     courses.append(course)
    #     amounts.append(amount)
    #     totalPrices.append(totalPrice)
    #     amount, course, totalPrice = 0, [], 0

    # """ 기획 case3: 1 Schedule = 1 Book 인 경우 """
    # amount, course, totalPrice = 0, [], 0
    # registerDates, statuses, courses, amounts, totalPrices, scheduleIds = [[] for _ in range(6)]
    # for schedule in schedules:
    #     registerDates.append(schedule.eventDate)
    #     statuses.append(schedule.status)
    #     books = Book.objects.filter(schedule=schedule)
    #     course.append(book.course)
    #     amount = book.amount
    #     totalPrice = book.totalPrice

    context = {}
    context['chef'] = chef
    context['post'] = post
    context['course'] = course
    context['scheduleList'] = scheduleInfoList

    return render(request, 'chefSchedule.html', context)


def chefScheduleDetail(request, schedule_id):
    return render(request, 'chefSchedule_detail.html')
