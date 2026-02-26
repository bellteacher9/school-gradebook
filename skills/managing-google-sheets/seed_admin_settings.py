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

def seed_admin_settings():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet("admin_settings")
        
        # Initial variables for 2026
        # Year, Variable, Value, Description
        seed_data = [
            [2026, "TERM_1_START_DATE", "2026-05-18", "Official start of Term 1"],
            [2026, "TERM_1_END_DATE", "2026-10-09", "Official end of Term 1"],
            [2026, "TERM_2_START_DATE", "2026-11-02", "Official start of Term 2"],
            [2026, "TERM_2_END_DATE", "2026-03-12", "Official end of Term 2"]
        ]
        
        # We append to avoid overwriting existing
        sheet.append_rows(seed_data)
        print("Seeded admin_settings with Term Date variables.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    seed_admin_settings()
