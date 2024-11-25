from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

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
            'password'
        )
        read_only_fields = ('terms_agreement', 'privacy_agreement')
