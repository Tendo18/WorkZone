from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

#EMPLOYER SERIALIZERS
class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        field = '__all__'

#APPLICANT SERIALIZERS
class ApplicantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        field = '__all__'

#JOB SERIALIZERS
class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        field = '__all__'

#APPLICATION SERIALIZERS
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        field = '__all__'