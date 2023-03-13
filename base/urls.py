from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_page, name='login'),
    path('register', views.register_page, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('room/<str:pk>/', views.room_page, name='room'),
    path('create_room/', views.create_room, name='create_room'),
    path('update_room/<str:pk>/', views.update_room, name='update_room'),
    path('profile/<str:pk>/', views.profile_page, name='profile'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete_room'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete_message'),

    path('update_user/<str:pk>/', views.update_user, name='update_user'),
    path('topics/', views.topics_page, name='topics_page'),

]
