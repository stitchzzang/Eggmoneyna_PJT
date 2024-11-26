from rest_framework import serializers
from .models import Thread, Comment
    
class ThreadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    comment_count = serializers.SerializerMethodField()
    member_type = serializers.CharField(source='user.member_type', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ('id', 'user', 'username', 'name', 'member_type', 'title', 'content', 
                 'created_at', 'updated_at', 'comment_count', 'likes_count', 'is_liked')
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_comment_count(self, obj):
        return obj.comment_set.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class ThreadListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comment_count = serializers.SerializerMethodField()
    member_type = serializers.CharField(source='user.member_type', read_only=True)

    
    class Meta:
        model = Thread
        fields = ('id', 'user', 'username', 'name', 'title', 'content', 
                 'member_type', 'created_at', 'likes_count', 'comment_count')
        
    def get_comment_count(self, obj):
        return obj.comment_set.count()

class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('title', 'content')

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    thread_title = serializers.CharField(source='thread.title', read_only=True)
    member_type = serializers.CharField(source='user.member_type', read_only=True)

    
    class Meta:
        model = Comment
        fields = ('id', 'thread', 'thread_title', 'content', 
                 'member_type', 'created_at', 'updated_at', 'username', 'name')
        read_only_fields = ('thread', 'user')

