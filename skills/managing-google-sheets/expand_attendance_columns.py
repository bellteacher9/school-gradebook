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

def expand_attendance_columns():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # BN to BU are columns 66 to 73 (Index 65 to 72)
        metrics = ["Attendance_Percent", "Absent_Count", "Late_Count", "Very_Late_Count"]
        t1_headers = [f"Term_01_{m}" for m in metrics]
        t2_headers = [f"Term_02_{m}" for m in metrics]
        all_new_headers = t1_headers + t2_headers
        
        # 1. Expand sheet (Current 70)
        body_expand = {
            "requests": [
                {
                    "appendDimension": {
                        "sheetId": sheet.id,
                        "dimension": "COLUMNS",
                        "length": 10 # 70 + 10 = 80
                    }
                }
            ]
        }
        spreadsheet.batch_update(body_expand)
        
        # 2. Add Headers BN1:BU1 (Index 65-72)
        sheet.update('BN1:BU1', [all_new_headers])
        print(f"Added detailed attendance headers.")
        
        # 3. Create Named Ranges
        add_nr_requests = []
        for i, name in enumerate(all_new_headers):
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
        print("Created named ranges for detailed attendance.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    expand_attendance_columns()
