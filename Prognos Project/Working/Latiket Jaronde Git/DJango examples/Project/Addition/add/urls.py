from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='add'),
    path('sum', views.sum, name='sum'),
    path('search',views.search, name="search"),
    path('uploadfile', views.uploadfile),
    path('indexfile', views.indexfile),
    path('searchpage', views.toSearchPage)
]
