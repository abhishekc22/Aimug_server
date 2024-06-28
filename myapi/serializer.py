from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ["username","email","password"]


class Loginseralizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'


class JobApplyingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_applying
        fields = ['user', 'Job_application', 'status']
      
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'created_at']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'