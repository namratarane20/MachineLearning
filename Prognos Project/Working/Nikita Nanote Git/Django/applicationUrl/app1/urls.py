from django.contrib import admin
from django.conf.urls import url
from app1 import views

urlpatterns = [
    url('first',views.view1),
    url('second',views.view2),
    url('third',views.view3),
    url('fourth',views.view4),
    url('fifth',views.view5),
]