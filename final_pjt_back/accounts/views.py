from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'GET':
        return Response({
            'message': '회원가입 페이지입니다.',
            'required_fields': {
                'username': '사용자 이름',
                'email': '이메일',
                'password1': '비밀번호',
                'password2': '비밀번호 확인',
                'name': '이름',
                'birth_date': '생년월일',
                'gender': '성별',
                'income_level': '소득 수준',
                'terms_agreement': '이용약관 동의',
                'privacy_agreement': '개인정보 처리방침 동의'
            }
        })
    
    # POST 요청 처리
    try:
         # username 중복 검사
        username = request.data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            return Response(
                {'error': '이미 사용 중인 아이디입니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 이메일 중복 검사
        email = request.data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            return Response(
                {'error': '이미 등록된 이메일입니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': '회원가입이 완료되었습니다.',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'member_type': user.member_type,
                },
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'GET':
        return Response({
            'message': '로그인 페이지입니다.',
            'required_fields': {
                'username': '사용자 이름',
                'password': '비밀번호'
            }
        })
    
    # POST 요청 처리
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
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'member_type': user.member_type
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    serializer = CustomUserDetailsSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    user = request.user
    
    # GET 요청 처리 추가
    if request.method == 'GET':
        return Response({
            'message': '회원정보 수정 페이지입니다.',
            'user_info': {
                'email': user.email,
                'birth_date': user.birth_date,
                'gender': user.gender,
                'income_level': user.income_level,
            }
        })
    
    # PUT 요청 처리
    password = request.data.get('password')
    email = request.data.get('email')
    birth_date = request.data.get('birth_date')
    gender = request.data.get('gender')
    income_level = request.data.get('income_level')
    
    # 비밀번호 변경
    if password:
        user.password = make_password(password)
    
    # 나머지 필드 업데이트
    if email:
        user.email = email
    if birth_date:
        user.birth_date = birth_date
    if gender:
        user.gender = gender
    if income_level:
        user.income_level = income_level
    
    try:
        user.save()
        return Response({'message': '회원정보가 성공적으로 업데이트되었습니다.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

