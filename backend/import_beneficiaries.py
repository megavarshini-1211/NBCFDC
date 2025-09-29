import os
import sys
import csv
from datetime import datetime

# --- This is the required setup to use Django's models in a standalone script ---

# 1. Add the project's root directory to Python's path
# This script is in the root, so its directory is the project root.
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# 2. Set the DJANGO_SETTINGS_MODULE environment variable
# Replace 'core.settings' with '<your_project_name>.settings' if different
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# 3. Setup Django
import django
django.setup()

# --- Now you can import your models and use them ---

from api.models import Beneficiary

def import_beneficiaries(file_path):
    """Reads a CSV file and imports data into the Beneficiary model."""
    print(f'Starting import from "{file_path}"...')
    
    created_count = 0
    updated_count = 0

    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip the header row

            for row in reader:
                beneficiary_id_val = row[0]
                
                # Format date and boolean values
                formatted_date = datetime.strptime(row[4], '%d-%m-%Y').strftime('%Y-%m-%d')
                is_default = (row[5] == '1')

                # Use update_or_create to avoid duplicates
                _, created = Beneficiary.objects.update_or_create(
                    beneficiary_id=beneficiary_id_val,
                    defaults={
                        'aadhar_number': row[1],
                        'mobile_number': row[2],
                        'full_name': row[3],
                        'date_of_birth': formatted_date,
                        'target_default': is_default,
                    }
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

    except FileNotFoundError:
        print(f'ERROR: File not found at "{file_path}"')
        return
    
    print(f'\nImport complete! {created_count} created, {updated_count} updated.')

if __name__ == '__main__':
    # Check if a file path was provided as a command-line argument
    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
        import_beneficiaries(csv_file_path)
    else:
        print("Please provide the path to the CSV file as an argument.")
        print("Usage: python standalone_import.py <path_to_file.csv>")