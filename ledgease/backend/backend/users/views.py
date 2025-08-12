from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, registrationSerializer, PortfolioSerializer
from .models import Portfolio
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

    
# This view will handle user registration requests
class registrationView(APIView):
    def post(self, request):
        serializer = registrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"ALERT": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)
    
# Handles user profile data
# This view will return the user's profile information
class userProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
# Placeholder for user portfolio view 
# This view will handle the user's portfolio data
class userPortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(qs, many=True)
        return Response(serializer.data)
    
class userSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"ALERT": "User settings updated successfully"}, status=200)
        return Response(serializer.errors, status=400)