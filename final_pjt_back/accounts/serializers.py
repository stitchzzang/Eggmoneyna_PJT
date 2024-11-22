from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

class UserCreateSerializer(serializers.ModelSerializer):
    # 약관 동의 필드 (임시 필드로 생성)
    terms_agreement = serializers.BooleanField(write_only=True)
    privacy_agreement = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'birth_date', 'name', 'member_type']
        extra_kwargs = {
            'password': {'write_only': True},
            'name': {'required': True},
            'birth_date': {'required': True}
        }
    
    def create(self, validated_data):
        password = validated_data['password']
        name = validated_data['name']
        birth_date = validated_data['birth_date']
        
        user = User.objects.create_user(
            password=password,
            name=name,
            birth_date=birth_date,
            **validated_data
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name', 'birth_date', 'member_type')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            name=validated_data['name'],
            birth_date=validated_data['birth_date'],
            member_type=validated_data.get('member_type', 'regular'),
            terms_agreement=validated_data.get('terms_agreement', False),
            privacy_agreement=validated_data.get('privacy_agreement', False),
        )
        return user
    