from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<pk>/', views.profile, name='profile'),
    # path('tag/<pk>', views.tag, name='tag'),
    path('post/<pk>', views.post, name='post'),
    path('likes', views.like, name='like'),
    path('register', views.register_request, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logout_profile, name='logout'),
    path('edit-profile', views.editProfile, name='edit-profile'),
    path('create-post', views.create_post, name='create-post'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]