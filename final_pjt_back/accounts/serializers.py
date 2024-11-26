from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from django.utils import timezone

class CustomRegisterSerializer(RegisterSerializer):
    # 필수 필드 추가
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=True)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)
    
    # 선택 필드 추가
    member_type = serializers.ChoiceField(
        choices=User.MEMBER_CHOICES, 
        default='regular',
        required=False
    )
    income_level = serializers.ChoiceField(
        choices=User.INCOME_CHOICES,
        default='middle',
        required=False
    )
    
    # 약관 동의 필드
    terms_agreement = serializers.BooleanField(required=True)
    privacy_agreement = serializers.BooleanField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'username': self.validated_data.get('username', ''),
            'birth_date': self.validated_data.get('birth_date', ''),
            'gender': self.validated_data.get('gender', ''),
            'member_type': self.validated_data.get('member_type', 'regular'),
            'income_level': self.validated_data.get('income_level', 'middle'),
            'terms_agreement': self.validated_data.get('terms_agreement', False),
            'privacy_agreement': self.validated_data.get('privacy_agreement', False),
        })
        return data


from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
UserModel = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    # 필수 필드
    email = serializers.EmailField()
    name = serializers.CharField()
    birth_date = serializers.DateField()
    gender = serializers.ChoiceField(choices=UserModel.GENDER_CHOICES)
    
    # 선택 필드
    member_type = serializers.ChoiceField(
        choices=UserModel.MEMBER_CHOICES,
        default='regular'
    )
    income_level = serializers.ChoiceField(
        choices=UserModel.INCOME_CHOICES,
        default='middle'
    )
    
    # 비밀번호 필드
    password = serializers.CharField(write_only=True, required=False)
    
    age = serializers.SerializerMethodField()
    total_score = serializers.IntegerField(read_only=True)
    test_date = serializers.DateTimeField(read_only=True)
    age_score = serializers.IntegerField(read_only=True)
    income_score = serializers.IntegerField(read_only=True)
    consumption_score = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = UserModel
        fields = (
            'pk', 
            'email',
            'name',
            'username',
            'birth_date',
            'gender',
            'member_type',
            'income_level',
            'terms_agreement',
            'privacy_agreement',
            'password',
            'age',
            'total_score',
            'test_date',
            'age_score',
            'income_score',
            'consumption_score'
        )
        read_only_fields = ('terms_agreement', 'privacy_agreement')

    def get_age(self, obj):
        today = timezone.now().date()
        birth_date = obj.birth_date
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age

    def calculate_scores(self, consumption_score):
        user = self.instance
        age = self.get_age(user)
        
        # 연령대 점수 계산
        if 20 <= age <= 39:
            age_score = 50
        elif 40 <= age <= 59:
            age_score = 100
        else:
            age_score = 75
            
        # 소득수준 점수 계산
        income_scores = {
            'low': 30,
            'middle': 60,
            'high': 100
        }
        income_score = income_scores[user.income_level]
        
        # 소비습관 점수 계산
        consumption_final_score = round((consumption_score/24)*50)
        
        # 최종 점수 계산
        final_score = round(age_score * 0.2 + income_score * 0.3 + consumption_final_score * 0.5)
        
        return {
            'age_score': age_score,
            'income_score': income_score,
            'consumption_score': consumption_final_score,
            'total_score': final_score
        }
