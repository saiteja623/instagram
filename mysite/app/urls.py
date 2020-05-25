from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('',views.home,name='home'),
    path('number',views.number,name='number')
]
