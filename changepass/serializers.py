from rest_framework import serializers
from user_management.models import*


#password reset serializers
class PasswordResetSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=32)
    user_phone_number = serializers.IntegerField()


#password reset otp code serializers
class OtpSerializer(serializers.Serializer):
    otp_pin = serializers.IntegerField()


#reset new password serializers
class ResetNewSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32)
    repert_password = serializers.CharField(max_length=32)


#country code serializers
class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'callingCodes']