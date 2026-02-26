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

def add_missing_cefr_summary_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        headers = [
            "Term_01_overall_cefr_letter",
            "Term_01_overall_cefr_class_average",
            "Term_02_overall_cefr_number",
            "Term_02_overall_cefr_class_average"
        ]
        
        # BN to BQ are columns 66 to 69 (0-indexed: 65 to 68)
        # 1-indexed range BN1:BQ1
        sheet.update('BN1:BQ1', [headers])
        print(f"Updated headers BN1:BQ1 for CEFR summary columns.")
        
        # 2. Create Named Ranges
        add_nr_requests = []
        for i, name in enumerate(headers):
            col_index = 65 + i
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
        print(f"Created named ranges for {headers}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_missing_cefr_summary_columns()
