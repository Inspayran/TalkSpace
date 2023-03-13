from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.relations import HyperlinkedIdentityField

from base.models import Room, Topic


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    def to_representation(self, instance):
        return instance.username


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

    def to_representation(self, instance):
        return instance.name


class RoomSerializer(serializers.ModelSerializer):
    host = UserSerializer()
    topic = TopicSerializer()
    url = HyperlinkedIdentityField(view_name='detail', lookup_field='pk')

    class Meta:
        model = Room
        fields = ['host', 'name', 'description', 'topic', 'url']


class RoomDetailSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    topic = TopicSerializer(label=False)
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_participants(self, obj):
        return UserSerializer(obj.participants.all(), many=True).data

    def update(self, instance, validated_data):
        topic_data = validated_data.pop('topic', None)
        if topic_data:
            topic_serializer = TopicSerializer(instance.topic, data=topic_data)
            topic_serializer.is_valid(raise_exception=True)
            topic_serializer.save()
        return super().update(instance, validated_data)




