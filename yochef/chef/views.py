from django.shortcuts import render

# Create your views here.

def registerChef(request, page_num):
    return render(request, f'registerChef_0{page_num}.html')