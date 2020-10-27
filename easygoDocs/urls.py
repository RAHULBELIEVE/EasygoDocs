"""easygoDocs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
import login.views as v


urlpatterns = [
     url(r'^admin/',admin.site.urls),
     url('',include("registration.urls")),
     url(r'^login/',v.loginreq,name='login'),
     url(r'^logout/',v.auth_logout,name='logout'),
     url(r'^reset/',v.log_password,name='reset'),
     url(r'^mail/',v.pass_email,name='mail'),
     url(r'^send_otp/',v.pass_otp,name='send_otp'),
     url(r'^sec_ques/',v.pass_sec,name='sec_ques'),
     url(r'^verify_otp/',v.verify_otp,name='verify_otp'),


     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)