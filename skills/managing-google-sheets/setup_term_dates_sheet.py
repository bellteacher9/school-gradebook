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

def setup_term_dates_sheet():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # 1. Create the sheet
        try:
            sheet = spreadsheet.add_worksheet(title="admin_term_dates", rows="100", cols="10")
            print("Created 'admin_term_dates' worksheet.")
        except gspread.exceptions.APIError as e:
            sheet = spreadsheet.worksheet("admin_term_dates")
            print("Worksheet 'admin_term_dates' already exists.")

        # 2. Set headers
        headers = ["year", "Term_Name", "Start_Date", "End_Date", "Description"]
        sheet.update(range_name='A1', values=[headers])
        
        # 3. Migrate seeded data from admin_settings if any
        # (For now, I'll just re-seed it with a cleaner structure)
        seed_data = [
            [2026, "Term 1", "2026-05-18", "2026-10-09", "Standard T1"],
            [2026, "Term 2", "2026-11-02", "2026-03-12", "Standard T2"]
        ]
        sheet.append_rows(seed_data)
        print("Seeded 'admin_term_dates' structure.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_term_dates_sheet()
