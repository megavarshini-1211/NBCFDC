# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GetBeneficiaryScore, BeneficiaryViewSet, LoanViewSet, EmiDetailViewSet,
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

# Define the URL patterns
urlpatterns = [
    # This includes all your previous model endpoints like /api/beneficiaries/
    path('', include(router.urls)), 
    
    # --- ADD THIS NEW URL PATTERN FOR THE CSV SCORE LOOKUP ---
    # This will handle requests like /api/score/NBC_001/
    path('score/<str:beneficiary_id>/', GetBeneficiaryScore.as_view(), name='get-score'),
]