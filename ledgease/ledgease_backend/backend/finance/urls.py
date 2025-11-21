from django.urls import path
from . import views

urlpatterns = [
    path('finance-categories/', views.categoryListCreateView.as_view(), name='category-list-create'),
    path('finance-categories/<int:pk>/', views.categoryDetailView.as_view(), name='category-detail'),
    path('finance-transactions/', views.transactionListCreateView.as_view(), name='transaction-list-create'),
    path('finance-transactions/<int:pk>/', views.transactionDetailView.as_view(), name='transaction-detail'),
    ]