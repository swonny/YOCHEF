from django.shortcuts import render

# Create your views here.
def main(request): 
    return render(request, "main.html")  #수정 필요 (확인 위해 작성)