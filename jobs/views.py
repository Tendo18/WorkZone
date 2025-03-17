from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

# Create your views here.
class EmployerView(APIView):
    def get(self, request):
        try:
            employer = Employer.objects.all()
            serializer =    EmployerSerializer(employer, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            serializer = EmployerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error : str(e)"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class EmployerDetailView(APIView):
    def get(self, request, id):
        try:
            employer = get_object_or_404 (Employer.objects.get(id=id))
            serializer = EmployerSerializer(employer)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, id):
        try:
            employer = get_object_or_404(Employer, id=id)
            serializer = EmployerSerializer(is_instance=employer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id):
        try:
            employer = get_object_or_404(Employer, id=id)
            employer.delete()
            return Response({"Message" : f" {employer.title} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class ApplicantsView(APIView):
    def get(self, request):
        try:
            applicants = Applicants.objects.all()
            serializer = ApplicantsSerializer(applicants, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            serializer = ApplicantsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ApplicantsDetailView(APIView):
    def get(self, request, id):
        try:
            applicants = get_object_or_404 (Applicants.objects.get(id=id))
            serializer = ApplicantsSerializer(applicants)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id):
        try:
            applicants = get_object_or_404 (Applicants, id=id)
            serializer = ApplicantsSerializer(is_instance=applicants, data=request.data, partial=True)
            if serializer.valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"Error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id):
        try:
            applicants = get_object_or_404(Applicants, id=id)
            applicants.delete()
            return Response({"Message" :f" {applicants.title} deleted successfully" }, status=status.HTTP_204_NO_CONTENT  )
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobsView(APIView):
    def get(self, request):
        try:
            jobs = Jobs.objects.all()
            serializer = JobsSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = JobsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"Error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class JobsDetailView(APIView):
    def get(self, request, id):
        try:
            jobs = get_object_or_404 (Jobs.objects.get(id=id))
            serializer = JobsSerializer(jobs)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            jobs = get_object_or_404 (Jobs, id=id)
            serializer = JobsSerializer(is_instance=jobs, data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            jobs = get_object_or_404 (Jobs, id=id)
            jobs.delete()
            return Response({"Message" :f" {jobs.title} deleted successfully" }, status=status.HTTP_204_NO_CONTENT  )
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ApplicationView(APIView):
    def get(self, request):
        try:
            application = Application.objects.all()
            serializer = ApplicationSerializer(application, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            serializer = ApplicationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ApplicationDetailView(APIView):
    def get(self, request, id):
        try:
            application = get_object_or_404(Application.objects.get(id=id))
            serializer = ApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            application = get_object_or_404(Application, id=id)
            serializer = ApplicationSerializer(is_instance=Application, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            application = get_object_or_404(Application, id=id)
            application.delete()
            return Response({"Message" :f" {application.title} deleted successfully" }, status=status.HTTP_204_NO_CONTENT  )
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

