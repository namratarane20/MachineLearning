from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home),
    # path("home/<str:name>", views.home),
    # path("home/<str:name>/<int:d>", views.out)
    path("home/<str:name>", views.home, name="homeurl"),
    path("home/<str:name>/<int:d>", views.out, name='outurl'),


]
