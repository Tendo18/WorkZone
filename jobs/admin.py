from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Employer)
admin.site.register(Applicants)
admin.site.register(Jobs)
admin.site.register(Application)