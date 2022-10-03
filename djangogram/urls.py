from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<pk>/', views.profile, name='profile'),
    path('tag/<pk>', views.tag, name='tag'),
    path('post/<pk>', views.post, name='post'),
    path('likes', views.like, name='like'),
]