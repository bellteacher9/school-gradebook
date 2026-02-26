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

def setup_holidays_sheet():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        try:
            sheet = spreadsheet.add_worksheet(title="admin_holidays", rows="100", cols="10")
        except gspread.exceptions.APIError:
            sheet = spreadsheet.worksheet("admin_holidays")

        headers = ["year", "Holiday_Name", "Start_Date", "End_Date", "Description"]
        sheet.update(range_name='A1', values=[headers])
        print("Created admin_holidays sheet.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_holidays_sheet()
