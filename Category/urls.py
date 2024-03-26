from django.urls import path
from .views import CategoryCreate

urlpatterns = [
    path('create/', CategoryCreate, name= 'category-create')
]