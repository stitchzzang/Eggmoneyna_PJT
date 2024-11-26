from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
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
                    'birth_date': user.birth_date,
                    'gender': user.gender,
                    'income_level': user.income_level,
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
        # Token 대신 JWT 사용
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'member_type': user.member_type,
                'birth_date': user.birth_date,
                'gender': user.gender,
                'income_level': user.income_level,
                'financial_score': user.financial_score,
            }
        })
    else:
        return Response({'error': '아이디 또는 비밀번호가 잘못되었습니다.'}, 
                      status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': '로그아웃되었습니다.'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': '로그아웃 실패'}, status=status.HTTP_400_BAD_REQUEST)


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
        # 이메일 중복 검사 추가
        if get_user_model().objects.exclude(pk=user.pk).filter(email=email).exists():
            return Response({'error': '이미 등록된 이메일입니다.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
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


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def calculate_financial_score(request):
#     user = request.user
#     consumption_score = request.data.get('totalScore')
    
#     if not consumption_score:
#         return Response({'error': '소비습관 점수가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     serializer = CustomUserDetailsSerializer(user)
#     scores = serializer.calculate_scores(consumption_score)
    
#     # 계산된 점수들을 DB에 저장
#     user.financial_score = scores['financial_score']
#     user.age_score = scores['age_score']
#     user.income_score = scores['income_score']
#     user.consumption_score = scores['consumption_score']
#     user.test_date = timezone.now()
#     user.save()
    
#     return Response(scores)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_financial_score(request):
#     serializer = CustomUserDetailsSerializer(request.user)
#     return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_financial_test(request):
    """
    금융성향 테스트 결과를 업데이트하는 뷰
    
    요청 데이터 형식:
    {
        "consumption_score": 24  # 소비습관 테스트 점수 (0-24점)
    }
    """
    try:
        # 현재 로그인한 사용자 가져오기
        user = request.user
        
        # 요청에서 소비습관 점수 가져오기
        consumption_raw_score = request.data.get('consumption_score')
        if consumption_raw_score is None:
            return Response(
                {'error': '소비습관 점수가 제공되지 않았습니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # UserDetailsSerializer 인스턴스 생성
        serializer = CustomUserDetailsSerializer(instance=user)
        
        # 점수 계산
        scores = serializer.calculate_scores(consumption_raw_score)
        
        # 사용자 정보 업데이트
        user.update_test_results(
            financial_score=scores['financial_score'],
            age_score=scores['age_score'],
            income_score=scores['income_score'],
            consumption_score=scores['consumption_score']
        )
        
        return Response({
            'message': '금융성향 테스트 결과가 성공적으로 업데이트되었습니다.',
            'scores': scores
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'테스트 결과 업데이트 중 오류가 발생했습니다: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

