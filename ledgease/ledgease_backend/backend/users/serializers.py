from django.contrib.auth.models import User
from django.core.exceptions import ValidationError as DjangoValidationError
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
class RegistrationSerializer(serializers.ModelSerializer):
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
    
# Serializer for changing user username, password, email
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=False, style={'input_type': 'new_password'})

    class Meta:
        model = User
        fields = ("username", "email", "password", "new_password") # new_password field for changing password

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists(): #Checks if email is user by another USER
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def validate(self, attrs):
        
        user = self.context["request"].user
        password = attrs.get("password")       
        new_password = attrs.get("new_password")

        
        if new_password:
            if not password: # If new password is provided, old password must be provided
                raise serializers.ValidationError(
                    {"password": "Old password is required to set a new password."}
                )

            if not user.check_password(password): # Check if old password is correct
                raise serializers.ValidationError(
                    {"password": "Old password is not correct."}
                )

            if password == new_password: # New password must be different from old password
                raise serializers.ValidationError(
                    {"new_password": "New password must be different from the old password."}
                )

            try: #Validate new password strength
                validate_password(new_password, user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError({"new_password": exc.messages})

        return attrs
    
    def update(self, instance, validated_data):
        #Change instances username and email
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        new_password = validated_data.get('new_password')
        if new_password: # If new password is provided, set the new password
            instance.set_password(new_password)
        instance.save() # Save the instance
        return instance # Returns updated saved user instance to save to database
        
    

        