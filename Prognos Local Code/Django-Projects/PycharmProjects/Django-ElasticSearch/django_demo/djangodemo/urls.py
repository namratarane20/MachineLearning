from django.contrib import  admin
from django.urls import  path
from  . import  views

urlpatterns = [
    # path('deleteUser', views.deleteUser),
    # path('addUser',views.addUser),
    #
    # path('demo',views.displayUser),

    path('', views.renderToLogin),
    path('userLogin', views.userLogin),
    path('searchKeyword', views.serachKeyword),
    path('uploadcsv', views.uploadcsv),
    path('homepage', views.toHomePage),
    path('indexfile', views.indexFile)
]
