from django.urls import path
from apiApp import views

urlpatterns = [
    path ('', views.landingpage, name = 'landingpage'),
    path ('home/', views.home, name = 'home'),
    path ('sign_up/', views.createUser, name = 'signup'),
    path ('log_in/', views.login, name = 'login'),
    path ('create_todo/', views.CreateList.as_view(), name = 'create'),
    path ('todos/', views.View.as_view(), name = 'list'),
    path ('update_todo/<int:id>/', views.Update.as_view, name = 'update'),
    path ('delete_todo/<int:id>/', views.Delete.as_view(), name = 'delete'),
]
