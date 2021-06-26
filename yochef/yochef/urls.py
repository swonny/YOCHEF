"""yochef URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import public.views # back 수정 필요 (html css 확인 목적으로 작성)
from django.conf.urls.static import static #static 연결 목적으로 작성
from django.conf import settings #static 연결 목적으로 작성

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', public.views.main, name = "main") # back 수정 필요 (html css 확인 목적으로 작성)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #static 연결 목적으로 작성