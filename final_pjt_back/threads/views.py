from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ThreadListSerializer, ThreadSerializer
from .models import Thread


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


# 모두 허용
@api_view(['GET'])
def thread_detail(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)

    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        print(serializer.data)
        return Response(serializer.data)

