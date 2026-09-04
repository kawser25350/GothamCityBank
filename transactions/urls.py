"""
URL configuration for bank_managment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from .views import WithdrawView,DepositeView,LoanRequstView,TransferMoneyView,TransactionReportView,LoanPaymentView

urlpatterns = [
   
    # path('register/',UserRegisterView.as_view(),name='register'),
    path('withdraw/',WithdrawView.as_view(),name='withdraw'),
    path('deposite/',DepositeView.as_view(),name='deposite'),
    path('loan_request/',LoanRequstView.as_view(),name='loan_request'),
    path('transfer_money/',TransferMoneyView.as_view(),name='transfer_money'),
    path('report/',TransactionReportView.as_view(),name='transaction_report'),
    path('loan/<int:pk>/pay/',LoanPaymentView.as_view(),name='loan_payment')
    
]
