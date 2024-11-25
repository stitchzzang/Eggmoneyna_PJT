from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ThreadListSerializer, ThreadSerializer, CommentSerializer
from .models import Thread, Comment


# 인증된 사용자만 사용 가능 : IsAuthenticated (요청에 반드시 토큰이 있어야 함)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def thread_list(request):
    if request.method == 'GET':  # 전체 게시글 조회 
        threads = get_list_or_404(Thread)
        serializer = ThreadListSerializer(threads, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':  # 게시글 생성  
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 단일 게시글 조회 (모두 허용)
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def thread_detail(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    
    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)
    
    # 작성자 확인
    if request.user != thread.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    elif request.method in ['PUT', 'PATCH']:  # PUT과 PATCH 모두 처리
        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    comments = Comment.objects.filter(thread=thread)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(
            thread=thread,
            user=request.user
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, thread_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 작성자 확인
    if request.user != comment.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['POST'])
def thread_like(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if thread.likes.filter(id=request.user.id).exists():
        thread.likes.remove(request.user)
        is_liked = False
    else:
        thread.likes.add(request.user)
        is_liked = True
    return Response({'is_liked': is_liked, 'like_count': thread.like_count})

