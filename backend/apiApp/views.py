from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from apiApp.models import *
from apiApp.forms import *
from apiApp.serializer import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.authtoken.models import Token

# Create your views here.

#landing page view
def landingpage (request):
    return render (request, 'apiApp/landing_page'.html)

#home view
@login_required (login_url= 'login')
def home (request):
    return render (request, 'apiApp/home.html')

#new sign_up view
def createUser (request):
    form = CreateUser
    if request.method == 'POST':
        form = CreateUser(request.post)
        if form.is_valid():
            form.save()
            return redirect ('login')
    form = CreateUser
    return render (request, 'registration/sign_up.html', {'form': form})

#log_in view
def login (request):
    form = Login
    if request.method == 'POST':
        form = Login(request.post)
        if form.is_valid():
            return redirect ('home')
    form = Login
    return render (request, 'registration/log_in.html', {'form': form})

#creating list
@login_required (login_url= 'login')
class CreateList (CreateView):
    form_class = Post
    context_object_name = 'form'
    template_name = 'apiApp/write_list.html'
    success_url = 'list'

#viewing list
@login_required (login_url= 'login')
class View (ListView):
    model = Todo
    context_object_name = 'list'
    template_name = 'apiApp/list.html'

#updating view
@login_required (login_url= 'login')
class Update (UpdateView):
    model = Todo
    form_class = Post
    success_url = 'list'
    template_name = 'apiApp/write_list.html'
    query_pk_and_slug = True
    pk_url_kwarg = 'id'
    queryset = Todo.objects.get(id)

#deleting view
@login_required (login_url= 'login')
class Delete (DeleteView):
    model = Todo
    query_pk_and_slug = True
    pk_url_kwarg = 'id'
    queryset = Todo.objects.get(id)
    success_url = 'list'
    template_name = 'apiApp/confirm_delete.html'

#now for serializers
#user creation serializer
class UserCreate (APIView):
    def post (self, request):
        first_name = request.data.get ('first_name')
        last_name = request.data.get ('last_name')
        username = request.data.get ('username')
        password = request.data.get ('password')
        email = request.data.get ('email')

        if not first_name or not last_name or not username or not password or not email:
            return Response ('Please provide all required fields', status.HTTP_400_BAD_REQUEST)

        user = CreateUser.objects.create_user (first_name = first_name, last_name = last_name, username = username, password = make_password(password), email = email)
        user.save()

        token, created = Token.objects.get_or_create (user=user)
        return Response ('User created successfully', status.HTTP_201_CREATED)
    
#user login serializer
class UserLogin (APIView):
    def post (self, request):
        username = request.data.get ('username')
        password = request.data.get ('password')

        if not username or not password:
            return Response ('Please provide all required fields', status.HTTP_400_BAD_REQUEST)

        user = authenticate (username = username, password = password)

        if user is not None:
            token, created = Token.objects.get_or_create (user = user)
            return Response ('Logged in successfully', status.HTTP_200_OK)
        else:
            return Response ('Invalid credentials', status.HTTP_400_BAD_REQUEST)