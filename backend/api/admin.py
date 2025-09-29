# api/admin.py

from django.contrib import admin
from .models import (
    Beneficiary, Loan, EmiDetail, AccountTransaction, 
    MobileRecharge, ElectricityBill, RationCard, PDSTransaction, UtilityBill
)

# --- Registering the core models ---

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('beneficiary_id', 'full_name', 'mobile_number', 'target_default')
    search_fields = ('full_name', 'beneficiary_id', 'aadhar_number')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'beneficiary', 'loan_scheme', 'original_loan_amount', 'sanction_date')
    search_fields = ('loan_id', 'beneficiary__full_name')

@admin.register(EmiDetail)
class EmiDetailAdmin(admin.ModelAdmin):
    list_display = ('emi_record_id', 'loan', 'emi_due_date', 'emi_amount', 'payment_status_detailed')
    search_fields = ('emi_record_id', 'loan__loan_id')

@admin.register(AccountTransaction)
class AccountTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'beneficiary', 'transaction_type', 'amount', 'transaction_timestamp')
    list_filter = ('transaction_type', 'mode')
    search_fields = ('transaction_id', 'beneficiary__full_name')

# --- Registering utility and spend models ---

@admin.register(MobileRecharge)
class MobileRechargeAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'operator_name', 'recharge_amount', 'bill_payment_date')
    search_fields = ('beneficiary__full_name',)

@admin.register(ElectricityBill)
class ElectricityBillAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'beneficiary', 'bill_amount', 'due_date', 'payment_status')
    search_fields = ('service_id', 'beneficiary__full_name')

@admin.register(UtilityBill)
class UtilityBillAdmin(admin.ModelAdmin):
    list_display = ('connection_id', 'beneficiary', 'utility_type', 'bill_amount', 'bill_due_date')
    list_filter = ('utility_type',)
    search_fields = ('connection_id', 'beneficiary__full_name')

# --- Registering PDS / Ration Card models ---

@admin.register(RationCard)
class RationCardAdmin(admin.ModelAdmin):
    list_display = ('ration_card_id', 'beneficiary', 'card_type', 'num_family_members')
    search_fields = ('ration_card_id', 'beneficiary__full_name')

@admin.register(PDSTransaction)
class PDSTransactionAdmin(admin.ModelAdmin):
    list_display = ('ration_card', 'item_name', 'transaction_date', 'uptake_ratio')
    search_fields = ('ration_card__ration_card_id',)