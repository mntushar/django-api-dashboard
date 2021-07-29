from django.urls import path
from .import views

urlpatterns = [
    #----> user authentication urls
    path('token/', views.user_token, name='create-token'), #create user token api url
    path('logout/', views.user_logout, name='user-logout'), #user logout api url


    #----> user password reset urls
    path('password_reset/', views.email_receive, name='passwore-reset-mail'), #user password reset mail api url
    path('password_set/', views.password_reset, name='new-passwore'), #user new password set api url



    
    
]