import gspread
from google.oauth2.service_account import Credentials
import sys
import os

# Define the scope
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Path to service account credentials
CREDENTIALS_PATH = os.path.join('.credentials', 'bell-474807-7b515f4c9f88.json')
SPREADSHEET_ID = '1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE'

def connect():
    try:
        if not os.path.exists(CREDENTIALS_PATH):
            print(f"Error: Credentials file not found at {CREDENTIALS_PATH}")
            sys.exit(1)
            
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        print(f"Successfully connected to spreadsheet: {spreadsheet.title}")
        
        # List all sheets (tabs)
        sheets = spreadsheet.worksheets()
        print("Available sheets:")
        for sheet in sheets:
            print(f"- {sheet.title} (ID: {sheet.id})")
            
        return spreadsheet
        
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        sys.exit(1)

if __name__ == "__main__":
    connect()
