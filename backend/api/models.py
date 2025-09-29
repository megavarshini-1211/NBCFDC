from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Beneficiary(models.Model):
    # Validators to ensure numbers are digits only
    numeric_validator = RegexValidator(r'^[0-9]*$', 'Only digit characters are allowed.')

    beneficiary_id = models.CharField(max_length=100, unique=True, help_text="Unique internal identifier (e.g., NBC_001)")
    aadhar_number = models.CharField(max_length=12, unique=True, validators=[numeric_validator])
    mobile_number = models.CharField(max_length=10, unique=True, validators=[numeric_validator])
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    target_default = models.BooleanField(default=False, help_text="False=Repaid/Non-Default, True=Default")
    
    # We add timestamps for good practice
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.beneficiary_id})"
    
class Loan(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='loans')
    loan_id = models.CharField(max_length=100, unique=True)
    loan_scheme = models.CharField(max_length=255)
    sanction_date = models.DateField()
    original_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_tenure_months = models.IntegerField()
    business_activity_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.loan_id

class EmiDetail(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='emis')
    emi_record_id = models.CharField(max_length=100, unique=True)
    emi_due_date = models.DateField()
    emi_paid_date = models.DateField(null=True, blank=True)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status_detailed = models.CharField(max_length=50)
    dpd_days = models.IntegerField(default=0, help_text="Days Past Due")

    def __str__(self):
        return self.emi_record_id


# --- 3. INFLOW/OUTFLOW TRANSACTIONS MODEL ---
class AccountTransaction(models.Model):
    TRANSACTION_TYPES = (('CREDIT', 'Credit'), ('DEBIT', 'Debit'))
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='transactions')
    account_number = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_timestamp = models.DateTimeField()
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)
    mode = models.CharField(max_length=50)
    merchant_category = models.CharField(max_length=100, null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    location_city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.transaction_id


# --- 4. MOBILE RECHARGE/SPEND MODEL ---
class MobileRecharge(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='recharges')
    operator_name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=50)
    bill_payment_date = models.DateField()
    recharge_amount = models.DecimalField(max_digits=8, decimal_places=2)
    validity_days = models.IntegerField()
    payment_source = models.CharField(max_length=50)
    is_auto_pay = models.BooleanField(default=False)
    data_usage_gb = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.beneficiary.full_name} - {self.bill_payment_date}"


# --- 5. ELECTRICITY BILL MODEL ---
class ElectricityBill(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='electricity_bills')
    service_id = models.CharField(max_length=100, unique=True)
    billing_cycle_start = models.DateField()
    billing_cycle_end = models.DateField()
    kwh_consumption = models.IntegerField()
    meter_reading_new = models.IntegerField()
    due_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=50)
    subsidy_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.service_id


# --- 6. PDS / RATION CARD MODELS ---
class RationCard(models.Model):
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, related_name='ration_card')
    ration_card_id = models.CharField(max_length=100, unique=True)
    card_type = models.CharField(max_length=50)
    num_family_members = models.IntegerField()
    # A JSONField (PostgreSQL) or a separate FamilyMember model would be more robust here.
    member_aadhar_list = models.TextField(help_text="Comma-separated list of Aadhar numbers", null=True, blank=True)

    def __str__(self):
        return self.ration_card_id

class PDSTransaction(models.Model):
    ration_card = models.ForeignKey(RationCard, on_delete=models.CASCADE, related_name='pds_transactions')
    transaction_date = models.DateField()
    item_name = models.CharField(max_length=100)
    allocated_quantity_kg = models.FloatField()
    actual_uptake_quantity_kg = models.FloatField()
    uptake_ratio = models.FloatField()

    def __str__(self):
        return f"{self.ration_card.ration_card_id} - {self.transaction_date}"


# --- 7. OTHER UTILITY BILLS MODEL ---
class UtilityBill(models.Model):
    UTILITY_CHOICES = (
        ('Water', 'Water'), ('Gas', 'Gas'), 
        ('Property Tax', 'Property Tax'), ('Sewerage', 'Sewerage')
    )
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='utility_bills')
    connection_id = models.CharField(max_length=100, unique=True)
    utility_type = models.CharField(max_length=20, choices=UTILITY_CHOICES)
    billing_period = models.CharField(max_length=50)
    bill_due_date = models.DateField()
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    arrears_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    metered_consumption = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.connection_id