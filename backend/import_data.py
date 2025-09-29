import os
import sys
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation

# --- REQUIRED DJANGO SETUP ---
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
import django
django.setup()
# --- END OF DJANGO SETUP ---

from api.models import (
    Beneficiary, Loan, EmiDetail, AccountTransaction, MobileRecharge,
    ElectricityBill, RationCard, PDSTransaction, UtilityBill
)

def get_beneficiary(beneficiary_id):
    """Safely retrieves a Beneficiary object or None if not found."""
    try:
        return Beneficiary.objects.get(beneficiary_id=beneficiary_id)
    except Beneficiary.DoesNotExist:
        print(f"  - WARNING: Beneficiary with ID '{beneficiary_id}' not found. Skipping row.")
        return None

# ... (All the import functions like import_repayment, import_transactions, etc., remain exactly the same as before) ...
def import_repayment(file_path):
    """Imports Loan and EmiDetail data from repayment.csv."""
    print(f"\nImporting Repayment data from '{file_path}'...")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            beneficiary = get_beneficiary(row[0])
            if not beneficiary:
                continue
            loan, _ = Loan.objects.update_or_create(
                loan_id=row[1],
                defaults={
                    'beneficiary': beneficiary, 'loan_scheme': row[2], 'sanction_date': row[3],
                    'original_loan_amount': Decimal(row[4]), 'loan_tenure_months': int(row[5]),
                })
            EmiDetail.objects.update_or_create(
                emi_record_id=row[7],
                defaults={
                    'loan': loan, 'emi_due_date': row[8], 'emi_paid_date': row[9] or None,
                    'emi_amount': Decimal(row[10]), 'payment_status_detailed': row[11], 'dpd_days': int(row[12]),
                })
    print("Repayment data import complete.")

def import_transactions(file_path):
    """Imports AccountTransaction data from transactions.csv."""
    print(f"\nImporting Account Transaction data from '{file_path}'...")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            beneficiary = get_beneficiary(row[0])
            if not beneficiary:
                continue
            AccountTransaction.objects.update_or_create(
                transaction_id=row[2],
                defaults={
                    'beneficiary': beneficiary, 'account_number': row[1], 'transaction_timestamp': row[3],
                    'transaction_type': row[4].upper(), 'amount': Decimal(row[5]), 'description': row[6],
                    'current_balance': Decimal(row[7]), 'mode': row[8], 'is_recurring': row[10].lower() == 'true',
                })
    print("Account Transaction data import complete.")

def import_recharge(file_path):
    """Imports MobileRecharge data from recharge.csv."""
    print(f"\nImporting Mobile Recharge data from '{file_path}'...")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            beneficiary = get_beneficiary(row[0])
            if not beneficiary:
                continue
            MobileRecharge.objects.get_or_create(
                beneficiary=beneficiary, operator_name=row[1], bill_payment_date=row[3],
                recharge_amount=Decimal(row[4]),
                defaults={
                    'plan_type': row[2], 'validity_days': int(row[5]),
                    'payment_source': row[6], 'is_auto_pay': row[7].lower() == 'true',
                })
    print("Mobile Recharge data import complete.")

def import_electricity(file_path):
    """Imports ElectricityBill data from electricity.csv."""
    print(f"\nImporting Electricity Bill data from '{file_path}'...")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            beneficiary = get_beneficiary(row[0])
            if not beneficiary:
                continue
            ElectricityBill.objects.update_or_create(
                service_id=row[1],
                defaults={
                    'beneficiary': beneficiary, 'billing_cycle_start': row[2], 'billing_cycle_end': row[3],
                    'kwh_consumption': int(row[4]), 'meter_reading_new': int(row[5]), 'due_date': row[6],
                    'bill_amount': Decimal(row[7]), 'payment_date': row[8] or None, 'payment_status': row[9],
                    'subsidy_amount': Decimal(row[10]),
                })
    print("Electricity Bill data import complete.")

def import_pds(file_path):
    """Imports RationCard and PDSTransaction data from pds.csv."""
    print(f"\nImporting PDS data from '{file_path}'...")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            beneficiary = get_beneficiary(row[0])
            if not beneficiary:
                continue
            ration_card, _ = RationCard.objects.update_or_create(
                ration_card_id=row[1],
                defaults={
                    'beneficiary': beneficiary, 'card_type': row[2],
                    'num_family_members': int(row[3]), 'member_aadhar_list': row[4],
                })
            PDSTransaction.objects.get_or_create(
                ration_card=ration_card, transaction_date=row[5], item_name=row[6],
                defaults={
                    'allocated_quantity_kg': float(row[7]), 'actual_uptake_quantity_kg': float(row[8]),
                    'uptake_ratio': float(row[9]),
                })
    print("PDS data import complete.")

def import_utilities(file_path):
    """Imports UtilityBill data from utilities.csv."""
    print(f"\nImporting Utility Bill data from '{file_path}'...")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            beneficiary = get_beneficiary(row[0])
            if not beneficiary:
                continue
            UtilityBill.objects.update_or_create(
                connection_id=row[1],
                defaults={
                    'beneficiary': beneficiary, 'utility_type': row[2], 'billing_period': row[3],
                    'bill_due_date': row[4], 'bill_amount': Decimal(row[5]), 'payment_date': row[6] or None,
                    'arrears_amount': Decimal(row[7]), 'metered_consumption': float(row[8]) if row[8] else None,
                })
    print("Utility Bill data import complete.")


# --- SCRIPT EXECUTION LOGIC ---
if __name__ == '__main__':
    importers = {
        'repayment': (import_repayment, 'repayment.csv'),
        'transaction': (import_transactions, 'transactions.csv'),
        'recharge': (import_recharge, 'recharge.csv'),
        'electricity': (import_electricity, 'electricity.csv'),
        'pds': (import_pds, 'pds.csv'),
        'utility': (import_utilities, 'utilities.csv'),
    }

    # Check if the user wants to run all importers
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'all':
        print("🚀 Starting bulk data import for all files...")
        for import_type, (import_func, filename) in importers.items():
            if os.path.exists(filename):
                import_func(filename)
            else:
                print(f"\n- WARNING: File '{filename}' not found. Skipping {import_type} import.")
        print("\n✅ All data imports are complete.")

    # Logic for importing a single file (remains the same)
    elif len(sys.argv) == 3:
        importer_type = sys.argv[1].lower()
        file_path = sys.argv[2]
        import_function, _ = importers.get(importer_type, (None, None))

        if not import_function:
            print(f"Error: Unknown importer type '{importer_type}'")
            sys.exit(1)
        
        import_function(file_path)

    else:
        print("Usage:")
        print("  To run all imports: python unified_import.py all")
        print("  To run a single import: python unified_import.py <type> <filename>")
        print(f"  Available types: {', '.join(importers.keys())}")
        sys.exit(1)