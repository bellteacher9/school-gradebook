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

def add_nickname_column():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # 1. Name the third column header 'nickname' (C1)
        sheet.update_cell(1, 3, 'nickname')
        print("Updated cell C1 to 'nickname'")
        
        # 2. Create the Named Range 'nickname' for column C (C:C)
        body = {
            "requests": [
                {
                    "addNamedRange": {
                        "namedRange": {
                            "name": "nickname",
                            "range": {
                                "sheetId": sheet.id,
                                "startRowIndex": 0,
                                "endRowIndex": 1000,
                                "startColumnIndex": 2,
                                "endColumnIndex": 3
                            }
                        }
                    }
                }
            ]
        }
        spreadsheet.batch_update(body)
        print("Created named range 'nickname' for column C")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_nickname_column()
