from django.conf import settings 
from django.core.mail import send_mail

def send_account_activation_email(email, email_token) : 
    subject = 'Your Account Needs To Be Verified!'
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi, Click On The Link To Activate Your Account - http://localhost:8000/auth/activate/{email_token}"

    send_mail(subject, message, email_from, [email])

def send_forget_password_email(email, token) : 
    subject = 'Reset Password Link'
    message = f"Hi, Click On The Link To Change Your Password - http://localhost:8000/auth/change-pass/{token}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])