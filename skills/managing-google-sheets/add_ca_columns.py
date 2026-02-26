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

def add_ca_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # 1. Name the columns H1 to K1
        ca_headers = ['CA_Q1', 'CA_Q2', 'CA_Q3', 'CA_Q4']
        # Columns H, I, J, K are indices 7, 8, 9, 10
        sheet.update('H1:K1', [ca_headers])
        print("Updated headers H1:K1 to CA_Q1, CA_Q2, CA_Q3, CA_Q4")
        
        # 2. Create Named Ranges
        add_nr_requests = []
        for i, name in enumerate(ca_headers):
            col_index = 7 + i
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
        print("Created named ranges for CA_Q1 to CA_Q4")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_ca_columns()
