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
        fields = ['id', 'title', 'content', 'author', 'created_at','image']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class Enquieyserializer(serializers.ModelSerializer):
    class Meta:
        model = EnquiryUser
        fields = '__all__'

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPPasswordSetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
            verified_user = VerifiedUser.objects.get(user=user)

            if verified_user.otp != otp:
                raise serializers.ValidationError('Invalid OTP.')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        except VerifiedUser.DoesNotExist:
            raise serializers.ValidationError('OTP verification record not found.')

        return data
    

class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        Admin.objects.create(user=user, user_role='admin')
        return user