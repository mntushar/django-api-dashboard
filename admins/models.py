from django.db import models
from django.contrib.auth.models import User


#user role table
class UserRole(models.Model):
    role = models.CharField(max_length = 100)
    permission_read = models.BooleanField()
    permission_edit = models.BooleanField()
    permission_write = models.BooleanField()
    permission_delete = models.BooleanField()
    superuser = models.BooleanField(default=False)


    def __str__(self):
        return self.role

#end user role table


#employ information table start
#employ address information table
class EmployAddressInfo(models.Model):
    house_no = models.CharField(max_length = 50)
    village_name = models.CharField(max_length = 50)
    post_office = models.CharField(max_length = 50)
    thana_name = models.CharField(max_length = 50)
    district_name = models.CharField(max_length = 50)
    employ_id = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.employ_id.first_name


#employ academic information table
class EmployAcademicInfo(models.Model):
    degree = models.CharField(max_length=100)
    last_passing_institution_name = models.CharField(max_length = 100)
    last_passing_year = models.DateField()
    employ_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.degree


#employ basic information table
class EmployBasicInfo(models.Model):
    name = models.CharField(max_length = 100)
    gender = models.CharField(max_length=6)
    date_of_birth = models.DateField()
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=100, unique=True, error_messages={'unique':"This email has already been registered."})
    employ_id = models.OneToOneField(User, on_delete=models.CASCADE)
        

    def __str__(self):
        return self.name


#employ employ information table
class EmployInfo(models.Model):
    password = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    user_basic = models.OneToOneField(EmployBasicInfo, on_delete=models.CASCADE)
    user_academic = models.OneToOneField(EmployAcademicInfo, on_delete=models.CASCADE)
    user_address = models.OneToOneField(EmployAddressInfo, on_delete=models.CASCADE)


    def __str__(self):
        return self.user_basic.name


#employ information table end


#user menu permission table start
#sidbar menu section
class SbSection(models.Model):
    section_title = models.CharField(max_length = 100, )


    def __str__(self):
        return self.section_title


#sidebar title table
class SbTitle(models.Model):
    sb_title = models.CharField(max_length = 100, )
    icone = models.CharField(max_length=100, )
    section_title = models.ForeignKey(SbSection, on_delete=models.PROTECT)
    user_role = models.ManyToManyField(UserRole, blank=True)


    def __str__(self):
        return self.sb_title


#sidebar title element table
class SbTitleElement(models.Model):
    el_title = models.CharField(max_length = 100, )
    url = models.CharField(max_length=200, )
    sbtitle_id = models.ForeignKey(SbTitle, on_delete=models.PROTECT)
    user_role = models.ManyToManyField(UserRole, blank=True)


    def __str__(self):
        return self.el_title

#user menu permission table end