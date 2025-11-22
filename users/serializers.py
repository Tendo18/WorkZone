from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import AdminProfile, EmployerProfile, ApplicantProfile
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_role_specific_welcome_email

User = get_user_model()

# Define role choices here to avoid import issues
ROLE_CHOICES = (
    ("admin", "Admin"),
    ("employer", "Employer"),
    ("applicant", "Applicant"),
)

# --- User Serializers ---

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'phone_number',
            'role', 'address', 'profile_image', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']

# --- Token Response Serializer ---
class TokenResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    access = serializers.CharField()
    refresh = serializers.CharField()

# --- Registration Serializers ---

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    profile_image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        required=False
    )

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'phone_number',
            'role', 'address', 'profile_image', 'password', 'confirm_password'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role = validated_data.get('role')
        user = User.objects.create_user(**validated_data)
        # Create role-specific profile
        if role == 'admin':
            AdminProfile.objects.create(user=user)
        elif role == 'employer':
            EmployerProfile.objects.create(user=user, company_name=validated_data.get('username', ''))
        elif role == 'applicant':
            ApplicantProfile.objects.create(user=user)
        
        # Send welcome email
        try:
            send_role_specific_welcome_email(user)
        except Exception as e:
            # Log the error but don't fail registration
            print(f"Failed to send welcome email: {str(e)}")
        
        return user

# --- Login Serializer ---

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        data['user'] = user
        return data

    def to_representation(self, instance):
        """Generate tokens and return user data with tokens"""
        user = instance['user']
        refresh = RefreshToken.for_user(user)
        return {
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

# --- Logout Serializer ---
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        try:
            RefreshToken(value)
            return value
        except Exception:
            raise serializers.ValidationError("Invalid refresh token.")

# --- Admin Profile Serializer ---
class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = AdminProfile
        fields = ['user', 'department', 'employee_id', 'permissions', 'created_at', 'updated_at']

# --- Employer Profile Serializer ---
class EmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = EmployerProfile
        fields = [
            'user', 'company_name', 'company_description', 'company_website',
            'company_logo', 'industry', 'company_size', 'founded_year',
            'is_verified_employer', 'created_at', 'updated_at'
        ]

# --- Applicant Profile Serializer ---
class ApplicantProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ApplicantProfile
        fields = [
            'user', 'date_of_birth', 'gender', 'headline', 'summary', 'experience_years',
            'education_level', 'skills', 'preferred_job_types', 'preferred_locations',
            'salary_expectation', 'linkedin_url', 'github_url', 'portfolio_url',
            'is_available_for_work', 'is_verified_applicant', 'created_at', 'updated_at'
        ]