from rest_framework import serializers
from .models import Job,Resume,JobApplication,JobSearch, JobBookmark
from django.core.validators import FileExtensionValidator

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        validators =FileExtensionValidator[(allowed_extensions = ['pdf', 'jpeg', 'png'])]
                      
class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model =JobApplication
        fields = "__all__"
        

