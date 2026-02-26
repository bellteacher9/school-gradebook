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

def add_cefr_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        skills = ["reading_number", "listening_number", "speaking_number", "writing_number", "use_of_english_number"]
        
        t1_headers = [f"Term_01_cefr_{skill}" for skill in skills]
        t2_headers = [f"Term_02_cefr_{skill}" for skill in skills]
        all_cefr_headers = t1_headers + t2_headers
        
        # Start at index 43 (Column AR)
        # 43 to 52 (10 columns)
        # In range notation: AR is 44th col? No, A=1, Z=26, AA=27, AQ=43. So AR=44.
        # Let's use index-based update to be safe or just AR1:BA1
        sheet.update('AR1:BA1', [all_cefr_headers])
        print(f"Updated headers AR1:BA1 for CEFR metrics.")
        
        # 2. Create Named Ranges
        add_nr_requests = []
        for i, name in enumerate(all_cefr_headers):
            col_index = 43 + i
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
        print(f"Created 10 named ranges for CEFR metrics.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_cefr_columns()
