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

def setup_database_key():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # 1. Name the first column header 'student_id'
        sheet.update_cell(1, 1, 'student_id')
        print("Updated cell A1 to 'student_id'")
        
        # 2. Create the Named Range 'student_id' for column A (A:A)
        # We use the batch_update to define a named range
        body = {
            "requests": [
                {
                    "addNamedRange": {
                        "namedRange": {
                            "name": "student_id",
                            "range": {
                                "sheetId": sheet.id,
                                "startRowIndex": 0,
                                "endRowIndex": 1000, # Initial buffer, can be expanded
                                "startColumnIndex": 0,
                                "endColumnIndex": 1
                            }
                        }
                    }
                }
            ]
        }
        spreadsheet.batch_update(body)
        print("Created named range 'student_id' for column A")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database_key()
