from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime


# Create your models here.
class User(AbstractUser):
    MEMBER_CHOICES = [
        ('regular', '일반회원'),
        ('expert', '전문가회원'),
    ]
    
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    INCOME_CHOICES = [
        ('low', '저소득층 (월 소득 200만원 이하)'),
        ('middle', '중소득층 (월 소득 200만원 ~ 700만원)'),
        ('high', '고소득층 (월 소득 700만원 이상)'),
    ]
    
    # username(아이디)과 password는 AbstractUser에 이미 포함되어 있음
    # email과 first_name도 AbstractUser에 있지만, 필수 필드로 변경
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    birth_date = models.DateField(
        default=datetime.date(1900, 1, 1)  # 1990년 1월 1일을 기본값으로 설정
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',
        verbose_name='성별'
    )
    member_type = models.CharField(
        max_length=10,
        choices=MEMBER_CHOICES,
        default='regular'
    )
    
    # 약관 동의 필드 추가
    # '서비스 이용약관 동의',
    terms_agreement = models.BooleanField(default=False)
    # '개인정보 처리방침 동의',
    privacy_agreement = models.BooleanField(default=False)
    agreement_date = models.DateTimeField(null=True, blank=True)
    
    # 자산 필드를 소득구간 선택으로 변경
    income_level = models.CharField(
        max_length=10,
        choices=INCOME_CHOICES,
        default='middle',
        verbose_name='소득수준'
    )
    
    # 금융성향 테스트 결과 필드 추가
    total_score = models.IntegerField(null=True, blank=True, verbose_name='금융성향 점수')
    age_score = models.IntegerField(null=True, blank=True, verbose_name='연령대 점수')
    income_score = models.IntegerField(null=True, blank=True, verbose_name='소득수준 점수')
    consumption_score = models.IntegerField(null=True, blank=True, verbose_name='소비습관 점수')
    test_date = models.DateTimeField(null=True, blank=True, verbose_name='테스트 진행일')
    
    def update_test_results(self, financial_score, age_score, income_score, consumption_score):
        """테스트 결과를 업데이트하는 메서드"""
        self.age_score = age_score
        self.income_score = income_score
        self.consumption_score = consumption_score
        self.total_score = financial_score + age_score + income_score + consumption_score
        self.test_date = timezone.now()
        self.save()
    
    # 필수 필드 설정
    REQUIRED_FIELDS = ['email', 'name', 'birth_date', 'gender']


from allauth.account.adapter import DefaultAccountAdapter
from django.utils import timezone

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        회원가입 시 User 인스턴스를 저장하는 메서드
        """
        data = form.cleaned_data
        
        # 기본 필드 처리
        email = data.get('email')
        username = data.get('username')
        
        # 추가 필드 처리
        name = data.get('name')
        birth_date = data.get('birth_date')
        gender = data.get('gender')
        member_type = data.get('member_type', 'regular')  # 기본값 regular
        income_level = data.get('income_level', 'middle')  # 기본값 middle
        
        # 필수 필드 설정
        user.email = email
        user.username = username
        user.name = name
        user.birth_date = birth_date
        user.gender = gender
        user.member_type = member_type
        user.income_level = income_level
        
        # 약관 동의 처리
        user.terms_agreement = True
        user.privacy_agreement = True
        user.agreement_date = timezone.now()
        
        # 비밀번호 처리
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
            
        if commit:
            user.save()
        return user
