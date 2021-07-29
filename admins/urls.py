from django.urls import path
from .import views

urlpatterns = [
    #----> user role urls
    path('createrole/', views.user_role_api, name='create-role'), #create user role api url
    path('rolelist/', views.user_role_list, name='role-list'), #create user role list api url
    path('updaterole/<pk>/', views.user_role_update, name='role-update'), #create user role update api url


    #----> employ role urls
    path('createemploy/', views.employ_create, name='employ-create'), #employ create api url
    path('updateemploy/<pk>/', views.employ_update, name='employ-update'), #employ update api url
    path('employlist/', views.list_employ, name='employ-list'), #employ list api url
]