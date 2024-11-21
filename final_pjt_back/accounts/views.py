from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
# @permission_classes([AllowAny])
def signup(request):
    try:
        # 패스워드 일치 여부 확인
        password = request.data.get('password1')
        password_confirmation = request.data.get('password2')
        
        if password != password_confirmation:
            return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 시리얼라이저로 유저 생성
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # 비밀번호 해싱
            user.set_password(password)
            user.save()
            
            # 토큰 생성
            token = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'token': {
                    'refresh': str(token),
                    'access': str(token.access_token),
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(e)  # 디버깅용 로그
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': '아이디와 비밀번호를 모두 입력해주세요.'}, 
                      status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })
    else:
        return Response({'error': '아이디 또는 비밀번호가 잘못되었습니다.'}, 
                      status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': '인증되지 않은 사용자입니다.'}, 
                      status=status.HTTP_401_UNAUTHORIZED)
    
    # 사용자의 토큰 삭제
    Token.objects.filter(user=user).delete()
    
    return Response({'message': '로그아웃되었습니다.'}, 
                  status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': '인증되지 않은 사용자입니다.'}, 
                      status=status.HTTP_401_UNAUTHORIZED)
    
    # 토큰 삭제
    Token.objects.filter(user=user).delete()
    # 사용자 삭제
    user.delete()
    
    return Response({'message': '계정이 성공적으로 삭제되었습니다.'}, 
                  status=status.HTTP_204_NO_CONTENT)


