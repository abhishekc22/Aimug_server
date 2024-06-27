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
        fields = '__all__'
      