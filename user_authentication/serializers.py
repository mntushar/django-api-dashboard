from rest_framework import serializers
from django.contrib.auth.models import User
from admins.models import*


#..........................user authentication serializer section start.................
#user basic serializers
class BasicSerializer(serializers.Serializer):
    user_id = serializers.EmailField()
    password = serializers.CharField(max_length=50)


#user logout serializers
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


#..........................user authentication serializer section end.................


#..........................User password reset serializer section start.................
#user password reset mail serializer
class PasswordResetMailSerializer(serializers.Serializer):
    email = serializers.EmailField()


#user new password  serializer
class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50)


#..........................User password reset serializer section end.................