from django.urls import path
from .import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('about-us',views.about,name='about-us'),
    path('contacts',views.contacts,name='contacts'),
    path('check_availability', views.check_availability, name='check_availability')
]