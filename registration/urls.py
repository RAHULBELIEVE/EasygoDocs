from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'registration'
urlpatterns = [
     url(r'^signup/$', views.CreateAccount, name="register"),
]