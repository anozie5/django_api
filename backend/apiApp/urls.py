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
    path ('api/', views.UserLogin.as_view(), name = 'api_login'),
    path ('api/view_users', views.ViewUsers.as_view(), name = 'api_view_users'),
    path ('api/input_user', views.UserCreate.as_view(), name = 'api_input_user'),
    path ('api/create_list', views.ListCreate.as_view(), name = 'api_list_create'),
    path ('api/view_list', views.ViewList.as_view(), name = 'api_view_list'),
    path ('api/update_todo/<int:id>/', views.UpdateList.as_view(), name = 'api_update'),
    path ('api/delete_todo/<int:id>/', views.DeleteList.as_view(), name = 'api_delete'),
]
