from rest_framework import serializers
from django.contrib.auth.models import User
from admins.models import*


#..........................user role serializer section start.................
#create user role serializers
class UserRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        exclude = ['superuser']


#..........................user role serializer section end.................


#..........................user authentication serializer section start.................
#user serializers
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['last_name']


#..........................user authentication serializer section end.................


#..........................employ serializer section start.................
#employ basic info serializers
class EmployBasicInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployBasicInfo
        exclude = ['employ_id']


#employ academic info serializers
class EmployAcademicInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployAcademicInfo
        exclude = ['employ_id']


#employ address serializers
class EmployAddressInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployAddressInfo
        exclude = ['employ_id']


#employ designation serializers
class DesignationSerializers(serializers.Serializer):
    id =  serializers.IntegerField()


#employ info serializers
class EmployInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployInfo
        fields = '__all__'


#employ list serializers
class EmployListSerializers(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='user_basic')
    email = serializers.StringRelatedField(source='user_basic.email')
    designation = serializers.StringRelatedField()
    class Meta:
        model = EmployInfo
        fields = ['id', 'name', 'email', 'designation']


#..........................employ serializer section end.................

