from rest_framework import serializers
from .models import Thread, Comment
    
class ThreadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'user', 'username', 'title', 'content', 
                 'created_at', 'updated_at', 'likes_count')
        read_only_fields = ('user', 'created_at', 'updated_at')

class ThreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('title', 'content')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'updated_at', 'user', 'post')
        read_only_fields = ('user',)

