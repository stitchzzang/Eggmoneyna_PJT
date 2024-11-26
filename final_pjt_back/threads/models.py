from django.db import models
from django.conf import settings

class Thread(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='threads'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_threads', blank=True)

    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comment_set.count()
    
    # username, name, member_type을 가져오기 위한 편의 메서드들
    @property
    def username(self):
        return self.user.username
    
    @property
    def name(self):
        return self.user.name
    
    @property
    def member_type(self):
        return self.user.member_type

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='comments'
    )
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def username(self):
        return self.user.username
    
    @property
    def name(self):
        return self.user.name
    
    @property
    def member_type(self):
        return self.user.member_type
    
    @property
    def thread_title(self):
        return self.thread.title
    
    @property
    def thread_content(self):
        return self.thread.content
