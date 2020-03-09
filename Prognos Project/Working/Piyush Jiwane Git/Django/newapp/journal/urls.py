from django.contrib import admin
from django.urls import path,include

from journal import views

urlpatterns = [
    path('',views.index,name='index')
]
