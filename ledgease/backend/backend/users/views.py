from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import UserSerializer, PortfolioSerializer, ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
# Create your views here.

# This view will handle the token generation for user authentication
class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer

# Handles user registration
# This serializer will create a new user with the provided data tracks username, email, password and created tag
class registerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
# This view will handle user registration requests on the frontend
class registrationView(APIView):
    def post(self, request):
        serializer = registerationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"ALERT": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)
    
# Handles user profile data on a frontend request
# This view will return the user's profile information
class userProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.username
        email = request.user.email
        serializer = UserSerializer(user, email, many=False)
        return Response(serializer.data)
    
# Placeholder for user portfolio view frontend request
# This view will handle the user's portfolio data
class userPortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        portfolio = user.portfolio_set.all()  
        serializer = PortfolioSerializer(portfolio, many=True)
        return Response(serializer.data)