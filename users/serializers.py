from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user_details', 'phone', 'gender', 'image']

    def get_user_details(self, obj):
        """Returns details of the associated user."""
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "email": obj.user.email,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name
        }


class Registerserializer(serializers.Serializer):
    password1 = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)
    username = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    class Meta:
        model = Profile
        fields = ['fullname', 'username', 'email', 'phone', 'gender', 'image', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password does not match')

        if data['username'].exists():
            raise serializers.ValidationError('Username already exists')
        return data

    def create(self, validated_data):        
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile.objects.create(
            user = user ,
            full_name = validated_data['fullname'],
            phone = validated_data['phone'],
            gender = validated_data['gender'],
            image = validated_data.get('image'),
        )

        return profile
    