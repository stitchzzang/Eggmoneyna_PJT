from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

class UserCreateSerializer(serializers.ModelSerializer):
    # 약관 동의 필드 (임시 필드로 생성)
    terms_agreement = serializers.BooleanField(write_only=True)
    privacy_agreement = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'birth_date', 'member_type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # password를 해시화하여 저장
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'name', 'birth_date')  # password1, password2 대신 password 사용
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # password1 대신 password 사용
        user = get_user_model().objects.create_user(
            password=password,
            **validated_data
        )
        return user