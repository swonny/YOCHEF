from django.shortcuts import render
from chef.models import *

# Create your views here.
def main(request): 
    
    isChef = int(request.GET.get('isChef', 0))
    posts = Post.objects.filter(isOpen = True).order_by('registerDate')

    return render(request, 'main.html', {'posts': posts, 'isChef': isChef}) 