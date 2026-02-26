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

def add_red_marks_column():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # 1. Name the seventh column header 'red_marks' (G1)
        sheet.update_cell(1, 7, 'red_marks')
        print("Updated cell G1 to 'red_marks'")
        
        # 2. Create the Named Range 'red_marks' for column G (G:G)
        body = {
            "requests": [
                {
                    "addNamedRange": {
                        "namedRange": {
                            "name": "red_marks",
                            "range": {
                                "sheetId": sheet.id,
                                "startRowIndex": 0,
                                "endRowIndex": 1000,
                                "startColumnIndex": 6,
                                "endColumnIndex": 7
                            }
                        }
                    }
                }
            ]
        }
        spreadsheet.batch_update(body)
        print("Created named range 'red_marks' for column G")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_red_marks_column()
