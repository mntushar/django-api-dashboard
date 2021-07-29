from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from admins.models import EmployInfo
from functools import wraps
from .models import*


#user role start
#write user role
def write_required(function):
    @wraps(function)
    def user_write(request, *args, **kwargs):
        profile =  request.user
        if profile.is_staff == True:
            role = request.user.employinfo.designation.permission_write
            if role == True:
                return function(request, *args, **kwargs)
            else:
                return render(request, 'errors/errors.html')
        else:
            return render(request, 'errors/errors.html')

    return user_write


#delete user role
def delete_required(function):
    @wraps(function)
    def delete_permission(request, *args, **kwargs):
        profile =  request.user
        if profile.is_staff == True:
            role = request.user.employinfo.designation.permission_delete
            if role == True:
                return function(request, *args, **kwargs)
            else:
                return render(request, 'errors/errors.html')
        else:
            return render(request, 'errors/errors.html')

    return delete_permission


#edit user role
def edit_required(function):
    @wraps(function)
    def edit_permission(request, *args, **kwargs):
        profile =  request.user
        if profile.is_staff == True:
            role = request.user.employinfo.designation.permission_edit
            if role == True:
                return function(request, *args, **kwargs)
            else:
                return render(request, 'errors/errors.html')
        else:
            return render(request, 'errors/errors.html')
    return edit_permission


#read user role
def read_required(function):
    @wraps(function)
    def read_permission(request, *args, **kwargs):
        profile =  request.user
        if profile.is_staff == True:
            role = request.user.employinfo.designation.permission_read
            if role == True:
                return function(request, *args, **kwargs)
            else:
                return render(request, 'errors/errors.html')
        else:
            return render(request, 'errors/errors.html')

    return read_permission
#user role end


'''....................................................................................................................
Name of user role decorator
    write decorator ----> @write_required
    delete decorator ----> @delete_required
    edit decorator ----> @edit_required
    read decorator ----> @read_required

...................................................................................................................'''
