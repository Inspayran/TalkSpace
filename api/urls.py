from django.urls import path
from . import views

urlpatterns = [
    path('', views.RoomView.as_view(), name='room_view'),
    path('detail/<str:pk>/', views.RoomDetailView.as_view(), name='detail')
    # path('create_room', views.CreateRoomView.as_view(), name='CreateRoomView'),
]