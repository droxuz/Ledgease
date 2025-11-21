from django.http import JsonResponse
from django.shortcuts import render
from .models import UserFinanceData, Category, Transaction
from .serializers import UserFinanceDataSerializer, CategorySerializer, TransactionSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# Allows APIView of GET and POST for category model
class categoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def create_category(self, serializer):
        serializer.save(user=self.request.user)

# Allows APIView of GET, PUT, DELETE for category model
class categoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
# Allows APIView of GET and POST for transaction model
class transactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date')
    
    def create_transaction(self, serializer):
        serializer.save(user=self.request.user)

# Allows APIView of GET, PUT, DELETE for transaction model
class transactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
# Allows APIView of GET for user finance data model
class userFinanceDataRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserFinanceDataSerializer
        
    def get_object(self):
        finance_data, created = UserFinanceData.objects.get_or_create(user=self.request.user)
        finance_data.CalculateTotals() #Recalculate totals on each fetch
        return finance_data