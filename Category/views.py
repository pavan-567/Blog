from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Category
from django.contrib import messages

# Create your views here.
# class CategoryCreate(CreateView) : 
#     model = Category
#     fields = "__all__"

#     def get_success_url(self) : 
#         messages.success(self.request, 'New Category Created!')
#         return reverse_lazy('home')
    
def CategoryCreate(request) : 
    name = request.POST.get('name')
    if Category.objects.filter(name= name).exists() : 
        messages.error(request, f'Category - {name} already exists') 
    else : 
        Category.objects.create(name= name)
        messages.success(request, f'New Category - {name} Successfully Created!')
    return redirect('home')