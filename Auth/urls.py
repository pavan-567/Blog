from django.urls import path 
from .views import Login, Logout, Register, Activate_Email, Forgot_Password, Change_Password, Verify_Email

urlpatterns = [
    path('login/', Login, name= 'login'),
    path('logout/', Logout, name= 'logout'),
    path('register/', Register, name= 'register'),
    path('activate/<str:email_token>/', Activate_Email, name= 'activate'),
    path('forgot-pass/', Forgot_Password, name= 'forgot-pass'),
    path('change-pass/<str:password_token>/', Change_Password, name= 'change-pass'),
    path('verify/', Verify_Email, name= 'verify-email')
]