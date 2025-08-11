from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Portfolio

# Serializer for user profile data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']

# Serializer for user portfolio data restrictions
class PortfolioSerializer(serializers.ModelSerializer):
    # Placeholder fields for portfolio data
    class Meta:
        model = Portfolio
        fields = '__all__'  


# Information for user registration
class registrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "date_joined")

    def create(self, validated_data):
        # This hashes the password correctly
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user