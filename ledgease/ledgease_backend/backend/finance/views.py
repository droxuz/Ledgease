from django.http import JsonResponse
from django.shortcuts import render
from .models import UserFinanceData, Category, Transaction
from .serializers import UserFinanceDataSerializer, CategorySerializer, TransactionSerializer
# Create your views here.

def get_finance_data(request): #User must be logged in
    user = request.user #User from request
    try:
        finance_data = UserFinanceData.objects.get(user=user)#Get user finance data
    except UserFinanceData.DoesNotExist:
        return JsonResponse({"error": "Finance data not found."}, status=404)

    serializer = UserFinanceDataSerializer(finance_data)
    return JsonResponse({
        'data': serializer.data
    })

def create_category(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return JsonResponse({'message': 'Category created successfully.', 'category': serializer.data}, status=201)
        return JsonResponse(serializer.errors, status=400)

def create_transaction(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return JsonResponse({'message': 'Transaction created successfully.', 'transaction': serializer.data}, status=201)
        return JsonResponse(serializer.errors, status=400)