from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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


# Serializer for user registration (handles validation and creation)
class registrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")])
    username = serializers.CharField(required=True,)
    class Meta:
        model = User
        fields = ("username", "email", "password")
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])  
        )
        try:
            validate_password(validated_data['password'], user)
        except serializers.ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})
        return user
    
# Serializer for changing user password
class changePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate_new_password(self, value):
        user = self.context['request'].user
        try:
            validate_password(value, user)
        except serializers.ValidationError as err:
            raise serializers.ValidationError(err.messages)
        return value

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({"new_password": "The new password must be different from the old password."})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    

        