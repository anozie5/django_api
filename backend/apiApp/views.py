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
from django.views import View
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
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('login')
    return render (request, 'registration/sign_up.html', {'form': form})

#log_in view
def login (request):
    form = Login
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            return redirect ('home')
    return render (request, 'registration/log_in.html', {'form': form})

#creating list
@login_required (login_url= 'login')
class CreateList (View):
    form = Need
    def post (self, request):
        form = Need (request.POST)
        if form.is_valid():
            form.save()
            return redirect ('list')
    
    def get (self, request):
        form = Need
        return render (request, 'apiApp/write_list.html', {'form' : form})

#viewing list
@login_required (login_url= 'login')
class View (View):
    def get (self, request):
        list = Todo.objects.all()
        return render (request, 'apiApp/list.html', {'lists': list})

#updating view
@login_required (login_url= 'login')
class Update(View):
    def post(self, request, pk):
        list = Todo.objects.get(pk=pk)
        form = Need(request.POST, instance=list)
        if form.is_valid():
            form.save()
            return redirect('list')

    def get(self, request, pk):
        list = Todo.objects.get(pk=pk)
        form = Need(instance=list)
        return render(request, 'apiApp/write_list.html', {'form': form})

#deleting view
@login_required (login_url= 'login')
class Delete (View):
    def post (self, request, pk):
        list = Todo.objects.get (pk = pk)
        list.delete()
        return redirect ('list')
    
    def get (self, request, pk):
        list = Todo.objects.get (pk = pk)
        return render (request, 'apiApp/confirm_delete.html', {'list': list})


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
            return Response ('Please provpke all required fields', status.HTTP_400_BAD_REQUEST)

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
            return Response ('Please provpke all required fields', status.HTTP_400_BAD_REQUEST)

        user = authenticate (username = username, password = password)

        if user is not None:
            token, created = Token.objects.get_or_create (user = user)
            return Response ('Logged in successfully', status.HTTP_200_OK)
        else:
            return Response ('Invalid credentials', status.HTTP_400_BAD_REQUEST)
        
#users view serailizer
@login_required (login_url= 'api_login')
class ViewUsers (APIView):
    def get (self, request):
        users = UserAccount.objects.all().values(exclude=['password'])
        serializer = UserAccountSerializer (users, many=True)
        return Response (serializer.data, status.HTTP_200_OK)

#user create serailizer
@login_required (login_url= 'api_login')
class UserCreate (APIView):
    def post (self, request):
        serializer = UserAccountSerializer (data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status.HTTP_201_CREATED)
        return Response ('Invalid inputs', status.HTTP_400_BAD_REQUEST)

#list create serializer
@login_required (login_url= 'api_login')
class ListCreate (APIView):
    def post (self, request):
        serializer = TodoSerializer (data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status.HTTP_201_CREATED)
        return Response ('Invalid inputs', status.HTTP_400_BAD_REQUEST)

#list view serailizer
@login_required (login_url= 'api_login')
class ViewList (APIView):
    def get (self, request):
        list = Todo.objects.all()
        serializer = TodoSerializer (list, many=True)
        return Response (serializer.data, status.HTTP_200_OK)

#update list serializer
@login_required (login_url= 'api_login')
class UpdateList (APIView):  
    def post (self, request, pk):
        try:
            list = Todo.objects.get(pk = pk)
        except Todo.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer (list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get (self, request, pk):
        try:
            list = Todo.objects.get(pk = pk)
        except Todo.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(list)
        return Response(serializer.data)

#delete list serializer
@login_required (login_url= 'api_login')
class DeleteList (APIView):
    def post (self, request, pk):
        try:
            list = Todo.objects.get (pk = pk)
        except Todo.DoesNotExist:
            return Response (status.HTTP_404_NOT_FOUND)
        list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)