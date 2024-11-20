from rest_framework import serializers
from .models import Thread

class ThreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
    
class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ('user', )