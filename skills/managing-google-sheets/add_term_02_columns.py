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

def add_term_02_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        skills = ["Listening", "Reading", "Speaking", "Writing", "Progress", "Use_of_English"]
        
        # Midterm Term 02
        mid_prefix = "Midterm_Term_02_"
        mid_headers = [mid_prefix + skill for skill in skills]
        mid_headers.extend(["Midterm_Term02_Score", "Midterm_Term02_Class-Average"])
        
        # Finals Term 02
        fin_prefix = "Finals_Term_02_"
        fin_headers = [fin_prefix + skill for skill in skills]
        fin_headers.extend(["Finals_Term02_Score", "Finals_Term02_Class-Average"])
        
        all_term_02_headers = mid_headers + fin_headers
        
        # Columns AB to AQ are indices 27 to 42 (1-based index)
        # In range notation: AB is 28th col
        sheet.update('AB1:AQ1', [all_term_02_headers])
        print(f"Updated headers AB1:AQ1 for Term 2 assessments.")
        
        # 2. Create Named Ranges
        add_nr_requests = []
        for i, header_name in enumerate(all_term_02_headers):
            col_index = 27 + i
            nr_name = header_name.replace("-", "_")
            add_nr_requests.append({
                "addNamedRange": {
                    "namedRange": {
                        "name": nr_name,
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
        print(f"Created 16 named ranges for Term 2.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_term_02_columns()
