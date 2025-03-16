from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from django.conf import settings

from .models import *
from .serializers import *

# Create your views here.
class EmployerView(APIView):
    def get(self, request):
        pass

class ApplicantsView(APIView):
    def get(self, request):
        pass

class JobsView(APIView):
    def get(self, request):
        pass

class ApplicationView(APIView):
    def get(self, request):
        pass

class EmployerDetail(APIView):