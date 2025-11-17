from django.urls import path
from . import views

urlpatterns = [
    path('user-finance-data/', views.get_finance_data, name='get_finance_data'), #Endpoint to get user finance data
    ]