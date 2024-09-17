from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('guest_book/', views.guest_book, name="guest_book"),
    path('guest_book/new/', views.post_new, name='post_new'),
    path('github/', views.github, name='github'),
    path('movie_finder/', views.movie_finder, name='movie_finder'),
    path('question_game/', views.question_game, name='question_game'),
    path('question_game/twenty_questions/', views.twenty_questions, name='twenty_questions'),
    path('question_game/twenty_questions/summary/', views.summary, name='summary'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register'),
    path('blog/', views.blog, name='blog'),
    path('blog_post/<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
]