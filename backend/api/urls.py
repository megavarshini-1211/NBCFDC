# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BeneficiaryViewSet, LoanViewSet, EmiDetailViewSet,
    AccountTransactionViewSet, MobileRechargeViewSet, ElectricityBillViewSet,
    RationCardViewSet, PDSTransactionViewSet, UtilityBillViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'beneficiaries', BeneficiaryViewSet, basename='beneficiary')
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'emis', EmiDetailViewSet, basename='emi')
router.register(r'transactions', AccountTransactionViewSet, basename='transaction')
router.register(r'recharges', MobileRechargeViewSet, basename='recharge')
router.register(r'electricity-bills', ElectricityBillViewSet, basename='electricity-bill')
router.register(r'ration-cards', RationCardViewSet, basename='ration-card')
router.register(r'pds-transactions', PDSTransactionViewSet, basename='pds-transaction')
router.register(r'utility-bills', UtilityBillViewSet, basename='utility-bill')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)), # Include the router-generated URLs
]