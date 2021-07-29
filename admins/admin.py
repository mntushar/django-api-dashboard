from django.contrib import admin
from .models import *


# Employ information registration
admin.site.register(UserRole)
admin.site.register(EmployInfo)
admin.site.register(EmployBasicInfo)
admin.site.register(EmployAcademicInfo)
admin.site.register(EmployAddressInfo)
admin.site.register(SbSection)
admin.site.register(SbTitle)
admin.site.register(SbTitleElement)