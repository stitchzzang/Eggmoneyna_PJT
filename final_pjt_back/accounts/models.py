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
    
    # username(아이디)과 password는 AbstractUser에 이미 포함되어 있음
    # email과 first_name도 AbstractUser에 있지만, 필수 필드로 변경
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    
    # 새로 추가할 필드
    birth_date = models.DateField(
        default=datetime.date(1900, 1, 1)  # 1990년 1월 1일을 기본값으로 설정
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
    
    # 필수 필드 설정
    REQUIRED_FIELDS = ['email', 'name', 'birth_date']

