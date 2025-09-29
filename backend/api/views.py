# api/views.py

from rest_framework import generics, viewsets
from .models import (
    Beneficiary, Loan, EmiDetail, AccountTransaction, 
    MobileRecharge, ElectricityBill, RationCard, PDSTransaction, UtilityBill
)
from .serializers import (
    BeneficiarySerializer, LoanSerializer, EmiDetailSerializer,
    AccountTransactionSerializer, MobileRechargeSerializer, ElectricityBillSerializer,
    RationCardSerializer, PDSTransactionSerializer, UtilityBillSerializer
)


class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer

# --- ADD NEW VIEWSETS FOR ALL OTHER MODELS ---

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class EmiDetailViewSet(viewsets.ModelViewSet):
    queryset = EmiDetail.objects.all()
    serializer_class = EmiDetailSerializer

class AccountTransactionViewSet(viewsets.ModelViewSet):
    queryset = AccountTransaction.objects.all()
    serializer_class = AccountTransactionSerializer

class MobileRechargeViewSet(viewsets.ModelViewSet):
    queryset = MobileRecharge.objects.all()
    serializer_class = MobileRechargeSerializer

class ElectricityBillViewSet(viewsets.ModelViewSet):
    queryset = ElectricityBill.objects.all()
    serializer_class = ElectricityBillSerializer

class RationCardViewSet(viewsets.ModelViewSet):
    queryset = RationCard.objects.all()
    serializer_class = RationCardSerializer

class PDSTransactionViewSet(viewsets.ModelViewSet):
    queryset = PDSTransaction.objects.all()
    serializer_class = PDSTransactionSerializer

class UtilityBillViewSet(viewsets.ModelViewSet):
    queryset = UtilityBill.objects.all()
    serializer_class = UtilityBillSerializer