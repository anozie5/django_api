from django import forms
from apiApp.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

#creating forms for models
#for account creation
class CreateUser (UserCreationForm):
    class Meta:
        model = UserAccount
        field = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

#for logging in
class Login (AuthenticationForm):
    class Meta:
        model = UserAccount
        field = ('username', 'password')

#for the todo list
class Post (forms.ModelForm):
    class Meta:
        model = Todo
        field = '__all__'
