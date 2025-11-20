from rest_framework import serializers  
from datetime import datetime
from .models import Transaction, UserFinanceData, Category

#Serializer for UserFinanceData model
class UserFinanceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFinanceData
        fields = [
            'income', 
            'balance', 
            'expenses_total', 
            'spending_total', 
            'last_updated'
        ]
        
    def validate_finance_data(self, data): #These fields should non-negative
        if data['income'] < 0:
            raise serializers.ValidationError("Income cannot be negative.")
        if data['expenses_total'] < 0: 
            raise serializers.ValidationError("Total expenses cannot be negative.")
        if data['spending_total'] < 0:
            raise serializers.ValidationError("Total spending cannot be negative.")
        return data

#Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'type', 
            'name'
        ]

    def validate_category(self, data): #Validate category data
        if data['type'] not in ['EXPENSE', 'SPENDING']:
            raise serializers.ValidationError("Invalid category type.")
        if not data['name']:
            raise serializers.ValidationError("Category name cannot be empty.")
        return data

#Serializer for Transaction model
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'type', 
            'amount', 
            'date', 
            'description', 
            'category'
        ]
        read_only_fields = [ 
            'date'
        ]
    
    def validate_transaction(self,data): #Validates transactions
        if data['type'] not in ['INCOME', 'EXPENSE','SPENDING']:
            raise serializers.ValidationError("Invalid transaction type.")
        if data['amount'] <= 0:
            raise serializers.ValidationError("Transaction amount must be a non-zero positive value.")
        if data['category'] is None:
            raise serializers.ValidationError("Transaction must have a category.")
        return data