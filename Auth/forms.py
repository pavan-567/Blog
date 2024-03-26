from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(UserCreationForm) : 
    class Meta :
        model = User 
        fields = ['name', 'username', 'email', 'password1', 'password2']

        def __init__(self, *args, **kwargs) : 
            super(UserForm, self).__init__(*args, **kwargs)

            for field in ['username', 'email', 'password1', 'password2'] : 
                self.fields[field].help_text = None 


class UserUpdationForm(forms.ModelForm) : 
    class Meta : 
        model = User 
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs) : 
        super(UserUpdationForm, self).__init__(*args, **kwargs)

        for field in ['username', 'email'] : 
            self.fields[field].help_text = None 