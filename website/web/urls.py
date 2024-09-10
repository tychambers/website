from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('guest_book/', views.guest_book, name="guest_book"),
    path('guest_book/new/', views.post_new, name='post_new'),
    path('github/', views.github, name='github'),
    path('movie_finder/', views.movie_finder, name='movie_finder'),
]