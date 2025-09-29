from rest_framework import serializers
from .models import (
    Beneficiary, Loan, EmiDetail, AccountTransaction, 
    MobileRecharge, ElectricityBill, RationCard, PDSTransaction, UtilityBill
)
# --- ADD THE NEW BENEFICIARY SERIALIZER ---

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = [
            'id', 
            'beneficiary_id', 
            'aadhar_number', 
            'mobile_number', 
            'full_name', 
            'date_of_birth', 
            'target_default',
            'created_at',
        ]

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class EmiDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmiDetail
        fields = '__all__'

class AccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTransaction
        fields = '__all__'

class MobileRechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileRecharge
        fields = '__all__'

class ElectricityBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityBill
        fields = '__all__'

class RationCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RationCard
        fields = '__all__'

class PDSTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDSTransaction
        fields = '__all__'

class UtilityBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityBill
        fields = '__all__'