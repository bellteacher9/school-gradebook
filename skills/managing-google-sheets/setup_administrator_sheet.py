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

def setup_administrator_sheet():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # 1. Create the 'administrator' sheet if it doesn't exist
        try:
            admin_sheet = spreadsheet.add_worksheet(title="administrator", rows="100", cols="20")
            print("Created 'administrator' worksheet.")
        except gspread.exceptions.APIError as e:
            if "already exists" in str(e):
                admin_sheet = spreadsheet.worksheet("administrator")
                print("Worksheet 'administrator' already exists.")
            else:
                raise e

        # 2. Set up initial headers for variables
        headers = [["Variable", "Value", "Description"]]
        admin_sheet.update('A1:C1', headers)
        print("Set up headers: Variable, Value, Description")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_administrator_sheet()
