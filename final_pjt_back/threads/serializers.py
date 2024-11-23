from rest_framework import serializers
from .models import Thread, Comment
    
class ThreadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ('id', 'user', 'username', 'title', 'content', 
                 'created_at', 'updated_at', 'likes_count', 'comment_count')
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_comment_count(self, obj):
        return obj.comment_set.count()

class ThreadListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Thread
        fields = ('id', 'user', 'username', 'title', 'content', 
                 'created_at', 'likes_count', 'comment_count')
        
    def get_comment_count(self, obj):
        return obj.comment_set.count()

class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('title', 'content')

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    thread_title = serializers.CharField(source='thread.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'thread', 'thread_title', 'content', 
                 'created_at', 'updated_at', 'username')
        read_only_fields = ('thread', 'user')

