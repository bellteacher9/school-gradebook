import gspread
from google.oauth2.service_account import Credentials
import sys
import os

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

CREDENTIALS_PATH = os.path.join('.credentials', 'bell-474807-7b515f4c9f88.json')
SPREADSHEET_ID = '1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE'

def add_year_to_admin_tables():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # We need to add 'year' to these sheets. 
        # admin_classes already has it.
        target_sheets = [
            "admin_settings", 
            "admin_grading_policies", 
            "admin_red_marks", 
            "admin_cefr_lookup"
        ]
        
        for sheet_name in target_sheets:
            sheet = spreadsheet.worksheet(sheet_name)
            headers = sheet.row_values(1)
            
            if "year" not in headers:
                # Insert 'year' at the beginning
                new_headers = ["year"] + headers
                sheet.update(range_name='A1', values=[new_headers])
                print(f"Added 'year' column to {sheet_name}")
            else:
                print(f"'year' already exists in {sheet_name}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_year_to_admin_tables()
