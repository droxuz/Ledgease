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
