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

def add_finals_term_01_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        prefix = "Finals_Term_01_"
        skills = ["Listening", "Reading", "Speaking", "Writing", "Progress", "Use_of_English"]
        headers = [prefix + skill for skill in skills]
        
        # Adding summary headers
        headers.append("Finals_Term01_Score")
        headers.append("Finals_Term01_Class-Average")
        
        # Columns T to AA are indices 19 to 26
        sheet.update('T1:AA1', [headers])
        print(f"Updated headers T1:AA1 to {', '.join(headers)}")
        
        # 2. Create Named Ranges (Replacing hyphens with underscores for Named Range IDs)
        add_nr_requests = []
        for i, header_name in enumerate(headers):
            col_index = 19 + i
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
        print(f"Created named ranges for {headers}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_finals_term_01_columns()
