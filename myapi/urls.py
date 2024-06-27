from django.urls import path
from . views import *

urlpatterns = [
    path('signup/',SignupView.as_view(), name='signup'),
    path('login/',Userlogin.as_view(), name='signup'),
    path('superuser/',SuperuserLoginView.as_view()),
    path('verifyotp/',VerifyOTP.as_view(),name='verification'),
    path('jobapplication/',JobApplicationCreateView.as_view(),name='jobapplication'),
    path('job-application_list/', JobApplicationList.as_view(), name='job_application_list_create'),
    path('jobupdate/<int:pk>/', JobApplicationUpdateAPIView.as_view(), name='jobapplication-update'),
    path('jobadelete/<int:pk>/', JobApplicationDeleteView.as_view(), name='jobapplication-delete'),
    path('userslist/', CustomUserListView.as_view(), name='user-list'),
    path('jobsapply/<int:job_id>/', ApplyForJobView.as_view(), name='apply_for_job'),



]