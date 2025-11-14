from django.db import models
from django.contrib.auth.models import User

#Model to store user's overall financial data
class UserFinanceData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="finance_profile")
    income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expenses_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    spending_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True) #Might keep IDK

    def __str__(self):
        return f"User {self.user_id} - Balance: {self.balance}"
    
    def CalculateTotals(self):
        from django.db.models import Sum, Q
        totals = self.user.transactions.aggregate( #Aggregate totals for expenses, spending, and income using query filters of EXPENSE, SPENDING, INCOME
            expenses_total=Sum('amount', filter=Q(type='EXPENSE')),
            spending_total=Sum('amount', filter=Q(type='SPENDING')),
            income=Sum('amount', filter=Q(type='INCOME'))
        )
        self.expenses_total = totals['expenses_total'] if totals['expenses_total'] is not None else 0
        self.spending_total = totals['spending_total'] if totals['spending_total'] is not None else 0
        self.income = totals['income'] if totals['income'] is not None else 0

        self.balance = self.income - (self.expenses_total + self.spending_total)
        self.save()

#Category model for categorizing expenses and spending
class Category(models.Model):
    class CategoryType(models.TextChoices): #Types of categories INCOME will not have categories rather be NULL
        EXPENSE = 'EXPENSE', 'Expense'
        SPENDING = 'SPENDING', 'Spending'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories") #Link category to user
    type = models.CharField(max_length=10, choices=CategoryType.choices) #Type of category
    name = models.CharField(max_length=50) # Max Lngth of category name

    def __str__(self):
        return f"Category {self.name} for User {self.user_id}" #Return string representation of category with user ID

#Transaction model for recording income, expenses, and spending
class Transaction(models.Model):
    class TransactionType(models.TextChoices): #Types of transactions 
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'
        SPENDING = 'SPENDING', 'Spending'


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions") #Link transaction to user
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="transactions", null='True',blank='True') #Link transaction to category for INCOME will NULL
    type = models.CharField(max_length=10, choices=TransactionType.choices) #Type of transaction
    amount = models.DecimalField(max_digits=12, decimal_places=2) #Amount of transaction
    date = models.DateTimeField(auto_now_add=True) #Date time of transaction
    description = models.CharField(max_length=255, blank=True) #Description of transaction

    def __str__(self):
        x = self.category.type if self.category else "No Category"
        return f"Transaction {self.id} for User {self.user_id} - Amount: {self.amount} ({x})"
    
