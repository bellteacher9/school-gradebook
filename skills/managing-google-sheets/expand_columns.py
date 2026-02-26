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

def expand_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # Current columns are 27, we need at least 43 (AQ). Let's go to 60.
        body = {
            "requests": [
                {
                    "appendDimension": {
                        "sheetId": sheet.id,
                        "dimension": "COLUMNS",
                        "length": 33 # 27 + 33 = 60
                    }
                }
            ]
        }
        spreadsheet.batch_update(body)
        print("Expanded column count to 60.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    expand_columns()
