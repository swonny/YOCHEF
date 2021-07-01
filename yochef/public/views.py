from django.shortcuts import redirect, render
from chef.models import *

# Create your views here.
def main(request): 
    posts = Post.objects.filter(isOpen = True).order_by('registerDate')

    return render(request, 'main.html', {'posts': posts}) 

def changePageVer(request):
    if request.user.customer.currentVer == 1:
        request.user.customer.currentVer = 0
    else : 
        request.user.customer.currentVer = 1
    request.user.customer.save()
    
    return redirect('/')
    