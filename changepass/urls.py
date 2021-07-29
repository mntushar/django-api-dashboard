from django.urls import path, include
from .import views

urlpatterns = [
    path('pass/', views.passchange, name='change-pass'), #user password change urls
    path('countrycode/', views.country_code, name='country-code'), #user password reset api urls
    path('resetpass/', views.send_otp, name='reset-pass'), #user password reset api urls
    path('otpreceive/', views.receive_otp, name='otp-receive'), #user password reset receive opt pin api urls
    path('resetnewpass/', views.password_reset, name='new-pass'), #user new password reset api urls
]