from django.shortcuts import render
from .models import *
from .serializer  import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import random
from django.core.mail import send_mail
from rest_framework import generics
import logging
logger = logging.getLogger(__name__)



class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(request.data)


        if serializer.is_valid():
            print(serializer.data,'56666666666')
            otp = ''.join(random.choices('0123456789', k=4))
            user_data = serializer.validated_data
            user = CustomUser.objects.create(
                email=user_data.get("email"),
                username=user_data.get("username"),
                password=make_password(user_data.get("password"))
                )
            user.save()
            self.send_otp_email(user.email, otp)
            verified_user = VerifiedUser.objects.create(user=user, otp=otp)
            data = {'userid': user.id}
            return Response(data=data, status=status.HTTP_201_CREATED)
        print(serializer.errors,'566666666666666666666666')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_otp_email(self, email, otp):
        subject = 'OTP Verification'
        message = f'Your OTP for verification is: {otp}'
        from_email = 'servicescc.002@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
    

   



class VerifyOTP(APIView):
    def post(self, request):
        print(request.data)
        try:
            user_id = request.data.get('userId')
            otp = request.data.get('otp')

            verified_user = VerifiedUser.objects.get(user_id=user_id)
            saved_otp = verified_user.otp
            
            if saved_otp == otp:
                # Mark user as verified
                user = CustomUser.objects.get(id=user_id)
                user.is_verified = True
                user.save()
                return Response(status=status.HTTP_200_OK, data={"message": "OTP verified successfully."})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Invalid OTP."})
        except (VerifiedUser.DoesNotExist, CustomUser.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "User or OTP not found."})

    


class Userlogin(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = Loginseralizer(data=data)
            if serializer.is_valid():
                print(serializer.data)
                email = serializer.data.get("email")
                password = serializer.data.get("password")

                user = authenticate(email=email, password=password)
                if user is not None:
                    return Response(
                        {
                            "message": "Login successful.",
                            "user_id": user.id,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Invalid email or password."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
               
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(
                {"message": "An error occurred."},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

class SuperuserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_superuser:
            return Response(
                {"error": "Only superusers are allowed to log in"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            "message": "Login successful",
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_200_OK)




class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer



class JobApplicationList(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    
class JobApplicationUpdateAPIView(APIView):
    def get(self, request, pk):
        try:
            job_application = JobApplication.objects.get(pk=pk)
            serializer = JobApplicationSerializer(job_application)
            return Response(serializer.data)
        except JobApplication.DoesNotExist:
            return Response({'error': 'Job application not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            job_application = JobApplication.objects.get(pk=pk)
        except JobApplication.DoesNotExist:
            return Response({'error': 'Job application not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobApplicationSerializer(job_application, data=request.data ,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JobApplicationDeleteView(generics.DestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    lookup_field = 'pk'



    


class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_verified = True)
    serializer_class = UserSerializer


class Cutomerupdate_delete(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(is_verified = True)
    serializer_class = UserSerializer



class ApplyForJobView(APIView):
    def post(self, request, job_id):
        try:
            job_posting = JobApplication.objects.get(id=job_id)
        except JobApplication.DoesNotExist:
            return Response({"error": "Job posting not found"}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'user': user.id,
            'Job_application': job_posting.id,
            'status': request.data.get('status', 'Pending')
        }

        serializer = JobApplyingSerializer(data=data)
        if serializer.is_valid():
            job_application = serializer.save()
            return Response({"message": "Application submitted successfully", "application_id": job_application.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BlogListCreate(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer



class EnquiryUserListCreateAPIView(APIView):
    def get(self, request, format=None):
        queryset = EnquiryUser.objects.all()
        serializer = Enquieyserializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = Enquieyserializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            subject = 'New Enquiry'
            message = f'New enquiry from {instance.username}. Email: {instance.email}'
            from_email = request.data.get('email', settings.DEFAULT_FROM_EMAIL)
            send_mail(subject, message, from_email, ['servicescc.002@gmail.com'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RequestPasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                
                # Generate a new OTP
                otp = ''.join(random.choices('0123456789', k=4))
                
                # Update or create a VerifiedUser record
                verified_user, created = VerifiedUser.objects.update_or_create(
                    user=user,
                    defaults={'otp': otp, 'is_verified': False}
                )

                # Send the OTP email
                self.send_otp_email(user.email, otp)
                
                return Response({'message': 'OTP sent to your email.'},status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def send_otp_email(self, email, otp):
        subject = 'OTP Verification'
        message = f'Your OTP for verification is: {otp}'
        from_email = 'servicescc.002@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)




class OTPPasswordSetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPPasswordSetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']


            try:
                user = CustomUser.objects.get(email=email)
                verified_user = VerifiedUser.objects.get(user=user)


                if verified_user.otp == otp:
                    # Update the user's password
                    user.password = make_password(new_password)
                    user.is_verified = True  # Optionally mark user as verified
                    user.save()

                    # Mark OTP as used or delete it if necessary
                    verified_user.is_verified = True
                    verified_user.save()


                    return Response({'message': 'Password updated successfully.'})
                else:
                    return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
            except VerifiedUser.DoesNotExist:
                return Response({'error': 'OTP verification record not found.'}, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class AdminSignupView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data,'******************')
        serializer = AdminSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors,'??????????????')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminloginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if Admin.objects.filter(user=user).exists():
                return Response({
                    "message": "Login successful",
                    "username": user.username,
                    "email": user.email
                    
                })
            else:
                return Response({'detail': 'Not an admin'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


class AdminExistsView(APIView):
    def get(self, request, *args, **kwargs):
        admin_exists = Admin.objects.filter(user_role='admin').exists()
        return Response({'admin_exists': admin_exists}, status=status.HTTP_200_OK)