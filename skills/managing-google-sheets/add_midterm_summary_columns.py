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

def add_midterm_summary_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # Headers can have hyphens, but Named Ranges cannot.
        headers = ["Midterm_Term01_Score", "Midterm_Term01_Class-Average"]
        
        # 1. Update Headers
        sheet.update('R1:S1', [headers])
        print(f"Updated headers R1:S1 to {', '.join(headers)}")
        
        # 2. Create Named Ranges (using underscore instead of hyphen)
        named_ranges = ["Midterm_Term01_Score", "Midterm_Term01_Class_Average"]
        add_nr_requests = []
        for i, name in enumerate(named_ranges):
            col_index = 17 + i
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
        print(f"Created named ranges for {named_ranges}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_midterm_summary_columns()
