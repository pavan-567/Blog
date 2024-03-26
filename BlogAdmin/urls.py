from django.urls import path 
from .views import *

urlpatterns = [
    path('', Index),
    path('pdf_view/', ViewPDF, name= 'pdf-view'),
    path('pdf_download/', DownloadPDF, name= 'pdf-download'),
    path('user_download/', DownloadUsersPDF, name= 'users-download'),
    path('user_view/', UsersPDF, name='users-pdf')
]