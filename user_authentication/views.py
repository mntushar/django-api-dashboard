#-->django import
from django_api_dashboard import settings
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, logout
#-->rest framework import
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import rest_framework
import io
#-->python import
from datetime import datetime, timezone, timedelta
import base64
#-->local module import
from .serializers import*


#..........................User token api authentication section start.................
#Third party Creating tokens manually function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    #convert to refresh token into base64 encode
    planetext = str(refresh)
    string_bytes = planetext.encode("ascii") 
    base64_bytes = base64.b64encode(string_bytes) 
    base64_string = base64_bytes.decode("ascii")
    return {
        'refresh': base64_string,
        'access': str(refresh.access_token),
    }


#user login and create api
@api_view(['POST'])
def user_token(request):
    if request.method == 'POST':
        #check to data json formate
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)


        #convert user id base64 to planetext
        base64_string = data['user_id']
        base64_bytes = base64_string.encode("ascii") 
        base64_bytes = base64.b64decode(base64_bytes) 
        planetext_user_id = base64_bytes.decode("ascii")
        data['user_id'] = planetext_user_id


        #convert password base64 to planetext
        base64_string = data['password']
        base64_bytes = base64_string.encode("ascii") 
        base64_bytes = base64.b64decode(base64_bytes) 
        planetext_password = base64_bytes.decode("ascii")
        data['password'] = planetext_password


        serializer = BasicSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['user_id'], password=serializer.data['password'])
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(token)
            else:
                return Response({'statue':'Incorrect user ID or password.'}, status=rest_framework.status.HTTP_404_NOT_FOUND)
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#user logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        print(request.user)
        #check to data json formate
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)

        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            #convert refresh token base64 to planetext
            base64_string = serializer.data['refresh']
            base64_bytes = base64_string.encode("ascii") 
            base64_bytes = base64.b64decode(base64_bytes) 
            refresh_token = base64_bytes.decode("ascii")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({'status':'Logout success'}, status=rest_framework.status.HTTP_200_OK)
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
#..........................User token api authentication section end.................


#..........................User password reset api section start.................
#receive mail for password reset
@api_view(['POST'])
def email_receive(request):
    if request.method == 'POST':
        #check to data json formate
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)


        serializer = PasswordResetMailSerializer(data=data)
        if serializer.is_valid():
            try:
                user_mail = EmployBasicInfo.objects.get(email=serializer.data['email'])
                if user_mail:
                    user = user_mail.employ_id
                    token = Token.objects.get_or_create(user=user)
                    token_obj = Token.objects.get(key=token[0])
                    now_time = datetime.now(timezone.utc)
                    token_time = token_obj.created
                    time_difference =  now_time - token_time 
                    token_time_dif = time_difference / timedelta(minutes=1)
                    #check create token time
                    if token_time_dif <= settings.reset_token_time:
                        from_mail = settings.EMAIL_HOST_USER
                        to_mail = serializer.data['email']
                        email_title = render_to_string('password_reset/email_title.txt')
                        msg_plain = render_to_string('password_reset/email.txt')
                        html_content = render_to_string('password_reset/password_reset_mail.html', {'name':user_mail, 'massage':msg_plain, 'token':token[0]})
                        text_content = strip_tags(html_content)
                        email = EmailMultiAlternatives(
                            email_title,
                            text_content,
                            from_mail,
                            [to_mail]
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send()
                        return Response({'status':'Mail send'}, status=rest_framework.status.HTTP_200_OK)
                    else:
                        token_obj.delete()
                        token = Token.objects.get_or_create(user=user)
                        from_mail = settings.EMAIL_HOST_USER
                        to_mail = serializer.data['email']
                        email_title = render_to_string('password_reset/email_title.txt')
                        msg_plain = render_to_string('password_reset/email.txt')
                        html_content = render_to_string('password_reset/password_reset_mail.html', {'name':user_mail,'massage':msg_plain, 'token':token[0]})
                        text_content = strip_tags(html_content)
                        email = EmailMultiAlternatives(
                            email_title,
                            text_content,
                            from_mail,
                            [to_mail]
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send()
                        return Response({'status':'Mail send'}, status=rest_framework.status.HTTP_200_OK)
            except:
                return Response({'status':'No user found'}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#receve token and new password
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def password_reset(request):
    user = request.user
    token = Token.objects.get_or_create(user=user)
    token_obj = Token.objects.get(key=token[0])
    now_time = datetime.now(timezone.utc)
    token_time = token_obj.created
    time_difference =  now_time - token_time 
    token_time_dif = time_difference / timedelta(minutes=1)
    if token_time_dif <= settings.reset_token_time:
        if request.method == 'POST':
            #check to data json formate
            json = JSONRenderer().render(request.data)
            stream = io.BytesIO(json)
            data = JSONParser().parse(stream)
            serializer = NewPasswordSerializer(data=data)
            if serializer.is_valid():
                #convert new password base64 to planetext
                base64_string = serializer.data['password']
                base64_bytes = base64_string.encode("ascii") 
                base64_bytes = base64.b64decode(base64_bytes) 
                new_password = base64_bytes.decode("ascii")
                user.set_password(new_password)
                user.save()
                return Response({'status':'New password is set'}, status=rest_framework.status.HTTP_200_OK)
            return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status':'Token time out'}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
#..........................User password reset api section end.................


