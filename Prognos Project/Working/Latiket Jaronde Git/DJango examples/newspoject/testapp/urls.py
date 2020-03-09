from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.news),
    path('movies/', views.moviesnews),
    path('sports/', views.snews),
    path('politics/', views.pnews)
]
