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

def add_cefr_letter_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # 1. Expand sheet if necessary (Current: 60, Need: 65+)
        body_expand = {
            "requests": [
                {
                    "appendDimension": {
                        "sheetId": sheet.id,
                        "dimension": "COLUMNS",
                        "length": 10 # 60 + 10 = 70
                    }
                }
            ]
        }
        spreadsheet.batch_update(body_expand)
        print("Expanded column count to 70.")

        # 2. Add Headers
        skills = ["reading_letter", "listening_letter", "speaking_letter", "writing_letter", "use_of_english_letter"]
        t1_headers = [f"Term_01_cefr_{skill}" for skill in skills]
        t2_headers = [f"Term_02_cefr_{skill}" for skill in skills]
        all_cefr_headers = t1_headers + t2_headers
        
        # Start at index 55 (Column BD)
        sheet.update('BD1:BM1', [all_cefr_headers])
        print(f"Updated headers BD1:BM1 for CEFR letter metrics.")
        
        # 3. Create Named Ranges
        add_nr_requests = []
        for i, name in enumerate(all_cefr_headers):
            col_index = 55 + i
            add_nr_requests.append({
                "addNamedRange": {
                    "namedRange": {
                        "name": name,
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": 0,
                            "endRowIndex": 1000,
                            "startColumnIndex": col_index,
                            "endColumnIndex": col_index + 1
                        }
                    }
                }
            })
        spreadsheet.batch_update({"requests": add_nr_requests})
        print(f"Created 10 named ranges for CEFR letter metrics.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_cefr_letter_columns()
