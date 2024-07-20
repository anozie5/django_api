from django.shortcuts import render, redirect
from rest_framework.response import Response
from apiApp.models import *
from apiApp.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.

#landing page view
def landingpage (request):
    return render (request, apiApp/landingpage.html)

#home view
@login_required (login_url= 'login', next = True)
def home (request):
    return render (request, apiApp/home.html)

#new sign_up view
def createUser (request):
    form = CreateUser
    if request.method == 'POST':
        form = CreateUser(request.post)
        if form.is_valid():
            form.save()
            return redirect ('login')
    form = CreateUser
    return render (request, 'apiApp/sign_up.html', {'form': form})

#log_in view
def login (request):
    form = Login
    if request.method == 'POST':
        form = Login(request.post)
        if form.is_valid():
            return redirect ('home')
    form = Login
    return render (request, 'apiApp/log_in.html', {'form': form})

#creating list
@login_required (login_url= 'login', next = True)
class CreateList (CreateView):
    form_class = Post
    context_object_name = 'form'
    template_name = 'apiApp/write.html'
    success_url = 'list'

#viewing list
@login_required (login_url= 'login', next = True)
class View (ListView):
    model = Todo
    context_object_name = 'list'
    template_name = 'apiApp/list.html'

#updating view
@login_required (login_url= 'login', next = True)
class Update (UpdateView):
    model = Todo
    form_class = Post
    success_url = 'list'
    template_name = 'apiApp/write.html'
    query_pk_and_slug = True
    pk_url_kwarg = 'pk'
    queryset = Todo.object.get(pk = 'pk')

#deleting view
@login_required (login_url= 'login', next = True)
class Update (DeleteView):
    model = Todo
    query_pk_and_slug = True
    pk_url_kwarg = 'pk'
    queryset = Todo.object.get(pk = 'pk')
    success_url = 'list'
    template_name = 'apiApp/confirm.html'