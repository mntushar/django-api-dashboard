from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError
import rest_framework
import io
from admins.decorator import*
from .serializers import*
from admins.models import*


#..........................User role api section start.................
#user role create api start
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@write_required
def user_role_api(request):
    if request.method == 'POST':
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = UserRoleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=rest_framework.status.HTTP_200_OK)
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#user role list api start
@api_view()
@permission_classes([IsAuthenticated])
@read_required
def user_role_list(request):
    role_list = UserRole.objects.exclude(superuser=True)
    serializer = UserRoleSerializers(role_list, many=True)
    return Response(serializer.data, status=rest_framework.status.HTTP_200_OK)


#user role update api start
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@edit_required
def user_role_update(request, pk):
    role = UserRole.objects.get(id=pk)
    if request.method == 'PUT':
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = UserRoleSerializers(role, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=rest_framework.status.HTTP_200_OK)
        return Response({'status':serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#..........................User role api section end.................


#..........................employ api section start.................
#create employ
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@write_required
def employ_create(request):
    if request.method == 'POST':
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        #data manipulate form json data
        try:
            employ_basic_info = data['basic_info']
            designation = data['designation']
            employ_academic_info = data['academic_info']
            employ_address = data['address']
            user_info = {
                'username':employ_basic_info['email'],
                'email':employ_basic_info['email'],
                'first_name':employ_basic_info['name'],
                'password':data['password']
            }
        except:
            return Response({'status':'wrong key name'}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
        #check validation in serializer
        user_info_serializer = UserSerializers(data=user_info)
        employ_basic_info_serializer = EmployBasicInfoSerializers(data=employ_basic_info)
        designation_serializer = DesignationSerializers(data=designation)
        employ_academic_info_serializer = EmployAcademicInfoSerializers(data=employ_academic_info, many=True)
        employ_address_serializer = EmployAddressInfoSerializers(data=employ_address)
        #validation errors
        is_valid_user_info_serializer = user_info_serializer.is_valid()
        is_valid_employ_basic_info_serializer = employ_basic_info_serializer.is_valid()
        is_valid_designation_serializer = designation_serializer.is_valid()
        is_valid_employ_academic_info_serializer = employ_academic_info_serializer.is_valid()
        is_valid_employ_address_serializer = employ_address_serializer.is_valid()
        if  is_valid_user_info_serializer and  is_valid_employ_basic_info_serializer and  is_valid_employ_academic_info_serializer and is_valid_employ_address_serializer and is_valid_designation_serializer:
            user_obj = user_info_serializer.save(is_staff=True)
            basic_info_obj = employ_basic_info_serializer.save(employ_id=user_obj)
            academic_obj = employ_academic_info_serializer.save(employ_id=user_obj)
            address_obj = employ_address_serializer.save(employ_id=user_obj)
            employinfo = {
                'password':user_obj.id,
                'designation':designation_serializer.data['id'],
                'user_basic':basic_info_obj.id,
                'user_academic':academic_obj[0].id,
                'user_address':address_obj.id
            }
            employinfo_serializer = EmployInfoSerializers(data=employinfo)
            if employinfo_serializer.is_valid():
                employinfo_serializer.save()
                return Response(status=rest_framework.status.HTTP_200_OK)
            return Response({'status':employinfo_serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
        status_errors = {
            'user_info_serializer_errors':user_info_serializer.errors,
            'employ_basic_info_error':employ_basic_info_serializer.errors,
            'designation_errors':designation_serializer.errors,
            'employ_academic_info_error':employ_academic_info_serializer.errors,
            'employ_address_error':employ_address_serializer.errors,
        }
        return Response({'status':status_errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#update employ info
@api_view(['put'])
@permission_classes([IsAuthenticated])
@edit_required
def employ_update(request, pk):
    employ_user = EmployInfo.objects.get(id=pk)
    print(employ_user)
    basic_info = employ_user.user_basic
    address = employ_user.user_address
    role = employ_user.designation
    academic_info = EmployAcademicInfo.objects.filter(id=pk)
    if request.method == 'PUT':
        json = JSONRenderer().render(request.data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        #data manipulate form json data
        try:
            employ_basic_info = data['basic_info']
            designation = data['designation']
            employ_academic_info = data['academic_info']
            employ_address = data['address']
        except:
            return Response({'status':'wrong key name'}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
        #check validation in serializer
        employ_basic_info_serializer = EmployBasicInfoSerializers(basic_info, data=employ_basic_info)
        designation_serializer = DesignationSerializers(data=designation)
        #employ_academic_info_serializer = EmployAcademicInfoSerializers(data=employ_academic_info, many=True)
        employ_address_serializer = EmployAddressInfoSerializers(address, data=employ_address)
        #validation errors
        is_valid_employ_basic_info_serializer = employ_basic_info_serializer.is_valid()
        is_valid_designation_serializer = designation_serializer.is_valid()
        #is_valid_employ_academic_info_serializer = employ_academic_info_serializer.is_valid()
        is_valid_employ_address_serializer = employ_address_serializer.is_valid()
        if  is_valid_employ_basic_info_serializer and is_valid_employ_address_serializer and is_valid_designation_serializer:
            employ_basic_info_serializer.save()
            #employ_academic_info_serializer.save()
            employ_address_serializer.save()
            employinfo = {
                'designation':designation_serializer.data['id'],
            }
            employinfo_serializer = EmployInfoSerializers(role, data=EmployInfo)
            if employinfo_serializer.is_valid():
                employinfo_serializer.save()
                return Response(status=rest_framework.status.HTTP_200_OK)
            return Response({'status':employinfo_serializer.errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)
        status_errors = {
            'employ_basic_info_error':employ_basic_info_serializer.errors,
            'designation_errors':designation_serializer.errors,
            #'employ_academic_info_error':employ_academic_info_serializer.errors,
            'employ_address_error':employ_address_serializer.errors,
        }
        return Response({'status':status_errors}, status=rest_framework.status.HTTP_400_BAD_REQUEST)


#employ list api view
@api_view()
@permission_classes([IsAuthenticated])
@read_required
def list_employ(request):
    employ_list = EmployInfo.objects.exclude(designation__superuser=True)
    serializer = EmployListSerializers(employ_list, many=True)
    return Response(serializer.data, status=rest_framework.status.HTTP_200_OK)


#..........................employ api section end.................
