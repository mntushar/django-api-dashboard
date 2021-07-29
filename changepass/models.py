from django.db import models
from user_management.models import*


#password reset opt code table
class OtpCode(models.Model):
    user = models.OneToOneField(Consumer,  on_delete=models.CASCADE)
    otp_code = models.IntegerField()
    create_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user)
