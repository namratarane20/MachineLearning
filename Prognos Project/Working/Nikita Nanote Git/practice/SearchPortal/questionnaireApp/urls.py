from django.urls import path
from . import views

urlpatterns = [
    path('', views.userLogin),
    path('mailVerification', views.mailVerification),
    path('searchKeyword', views.searchKeyword),
    path('uploadcsv', views.uploadcsv),
    path('homepage', views.toHomePage),
    path('indexfile', views.indexToElasticsearch)
]
