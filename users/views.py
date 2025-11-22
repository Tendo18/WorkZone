from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer,
    AdminProfileSerializer, EmployerProfileSerializer, ApplicantProfileSerializer
)
from .models import AdminProfile, EmployerProfile, ApplicantProfile

User = get_user_model()

# --- Registration View ---
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Login View ---
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# --- Logout View ---
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh_token']
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- User Profile View ---
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Admin Profile View ---
class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            profile = AdminProfile.objects.get(user=request.user)
            serializer = AdminProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AdminProfile.DoesNotExist:
            return Response({'error': 'Admin profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        try:
            profile = AdminProfile.objects.get(user=request.user)
            serializer = AdminProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdminProfile.DoesNotExist:
            return Response({'error': 'Admin profile not found.'}, status=status.HTTP_404_NOT_FOUND)

# --- Employer Profile View ---
class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            profile = EmployerProfile.objects.get(user=request.user)
            serializer = EmployerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Employer profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        try:
            profile = EmployerProfile.objects.get(user=request.user)
            serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Employer profile not found.'}, status=status.HTTP_404_NOT_FOUND)

# --- Applicant Profile View ---
class ApplicantProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            profile = ApplicantProfile.objects.get(user=request.user)
            serializer = ApplicantProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ApplicantProfile.DoesNotExist:
            return Response({'error': 'Applicant profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        try:
            profile = ApplicantProfile.objects.get(user=request.user)
            serializer = ApplicantProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ApplicantProfile.DoesNotExist:
            return Response({'error': 'Applicant profile not found.'}, status=status.HTTP_404_NOT_FOUND)