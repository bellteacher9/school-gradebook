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

def apply_year_validation():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # Apply data validation to Column D (year), starting from row 2
        # We'll use a regex or a simple number range. Let's use a number range 2000-2100.
        body = {
            "requests": [
                {
                    "setDataValidation": {
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": 1,
                            "endRowIndex": 1000,
                            "startColumnIndex": 3,
                            "endColumnIndex": 4
                        },
                        "rule": {
                            "condition": {
                                "type": "NUMBER_BETWEEN",
                                "values": [
                                    {"userEnteredValue": "2000"},
                                    {"userEnteredValue": "2100"}
                                ]
                            },
                            "inputMessage": "Please enter a valid calendar year (e.g., 2026).",
                            "strict": True,
                            "showCustomUi": True
                        }
                    }
                }
            ]
        }
        spreadsheet.batch_update(body)
        print("Applied calendar year validation (2000-2100) to column D")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    apply_year_validation()
