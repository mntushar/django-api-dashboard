from ecommerce import settings
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from twilio.rest import Client
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import rest_framework
import io
from datetime import datetime, timezone, timedelta
import random as r
from changepass.forms import*
from changepass.models import*
from .serializers import*
from user_management.models import*


#change password 
@login_required()
def passchange(request):
    form = ChangePasswordForm()
    print(request.user.id)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            user_id = request.user
            if check_password(old_pass, user_id.password):
                new_pass = form.cleaned_data['new_pass']
                repeat_pass = form.cleaned_data['repert_new_pass']
                if new_pass == repeat_pass:
                    admin_old_password_obj = Consumer.objects.get(user=user_id.id)
                    admin_old_password_obj.password = new_pass
                    admin_old_password_obj.save()
                    user_auth = User.objects.get(id=user_id.id)
                    user_auth.set_password(new_pass)
                    user_auth.save()
                    return redirect('/home/login/')
                password_match_error = 'New password is not same'
                context = {
                    'form':form,
                    'password_match_error': password_match_error,
                }
                return render(request, 'backend/home/changepassword.html', context)
            password_match_error = 'Old password is wrong'
            context = {
                'form':form,
                'password_match_error': password_match_error,
            }
            return render(request, 'backend/home/changepassword.html', context)
        context = {
            'form':form,
        }
        return render(request, 'backend/home/changepassword.html', context)


    context = {
        'form':form,
    }
    return render(request, 'backend/home/changepassword.html', context)


#password reset by otp start
#otp code generate
def otpgen():
    otp=""
    for i in range(4):
        otp+=str(r.randint(1,9))
    return(otp)


#country code list form database
@api_view()
def country_code(request):
    all_country_code = Country.objects.all()
    serializer = CountryCodeSerializer(all_country_code, many=True)
    print(serializer.data)
    return Response({'Country name and phone code':serializer.data})


#send otp to user for reset
@api_view(['POST'])
def send_otp(request):
    if request.method == 'POST':
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = PasswordResetSerializer(data=data)
        if serializer.is_valid():
            phone_number = serializer.data['user_phone_number']
            country_code = serializer.data['country_code']
            try:
                user_info = Consumer.objects.get(phone=phone_number)
            except:
                return Response()
            if user_info:
                otp = otpgen()
                otp_user = None
                try:
                    otp_user = OtpCode.objects.get(user=user_info.id)
                except:
                    otp_user_obj = OtpCode.objects.create(
                        user=user_info,
                        otp_code=otp,
                    )
                    otp_user_obj.save()
                    #add to otp other services
                    '''messages_body = 'Your pin code is:' + otp
                    account_sid = "AC48bcccb265c1f3299ed9fc7dbae36891"
                    # Your Auth Token from twilio.com/console
                    auth_token  = "9b0e46962622b5978a14278babec79dd"

                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        to="+8801521475333", 
                        from_="+8801521477032",
                        body=messages_body)

                    print(message.sid)'''
                    return Response()
                if otp_user:
                    otp_user.otp_code = otp
                    otp_user.save()
                     #add to otp other services
                    '''messages_body = 'Your pin code is:' + otp
                    account_sid = "AC48bcccb265c1f3299ed9fc7dbae36891"
                    # Your Auth Token from twilio.com/console
                    auth_token  = "9b0e46962622b5978a14278babec79dd"

                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        to="+8801521475333", 
                        from_="+8801521477032",
                        body=messages_body)

                    print(message.sid)'''
                    return Response()
                return Response()
            return Response()
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#receive otp code forms user
@api_view(['POST'])
def receive_otp(request):
    if request.method == 'POST':
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = OtpSerializer(data=data)
        if serializer.is_valid():
            otp_pin = serializer.data['otp_pin']
            try:
                user_otp = OtpCode.objects.get(otp_code=otp_pin)
            except:
                return Response({'status':'You enter wrong pin'}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
            if user_otp:
                now_time = datetime.now(timezone.utc)
                otp_pin_time = user_otp.create_date
                time_difference = now_time - otp_pin_time 
                pin_time_dif = time_difference / timedelta(minutes=1)
                if pin_time_dif <= settings.reset_otp_pin_time:
                    user_info = Consumer.objects.get(id=user_otp.user.id)
                    user = User.objects.get(id=user_info.user.id)
                    token = Token.objects.get_or_create(user=user)
                    token_obj = Token.objects.get(key=token[0])
                    now_time = datetime.now(timezone.utc)
                    token_time = token_obj.created
                    time_difference =  now_time - token_time 
                    token_time_dif = time_difference / timedelta(minutes=1)
                    if token_time_dif <= settings.reset_token_time:
                        return Response({'Token':str(token_obj)}, status=rest_framework.status.HTTP_200_OK)
                    else:
                        token_obj.delete()
                        token = Token.objects.get_or_create(user=user)
                        token_obj = Token.objects.get(key=token[0])
                        return Response({'Token':str(token_obj)}, status=rest_framework.status.HTTP_200_OK)
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#user password reset
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def password_reset(request):
    if request.method == 'POST':
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = ResetNewSerializer(data=data)
        if serializer.is_valid():
            new_pass = serializer.data['password']
            repert_new_pass = serializer.data['repert_password']
            if new_pass==repert_new_pass:
                auth_user = request.user
                token_obj = Token.objects.get(user=auth_user)
                now_time = datetime.now(timezone.utc)
                token_time = token_obj.created
                time_difference =  now_time - token_time 
                token_time_dif = time_difference / timedelta(minutes=1)
                if token_time_dif <= settings.reset_token_time:
                    user_info = Consumer.objects.get(user=auth_user.id)
                    user_info.password = new_pass
                    user_info.save()
                    auth_user.set_password(new_pass)
                    auth_user.save()
                    return Response({'status':'Your password is Reset'}, status=rest_framework.status.HTTP_200_OK)
                else:
                    return Response({'status':'Please submite correct Token'}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
            return Response({'status':'New password is not same'}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
    return Response()


#password reset by otp end