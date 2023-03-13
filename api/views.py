from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from base.models import Room
from .serializers import RoomSerializer, CustomPagination, RoomDetailSerializer


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = CustomPagination


# class RoomDetailView(generics.RetrieveUpdateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomDetailSerializer
#     lookup_field = 'pk'


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# class CreateRoomView(generics.CreateAPIView):
#
