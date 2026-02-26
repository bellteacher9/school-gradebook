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

def restructure_database():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # 1. Update Headers to new order
        # A: student_id, B: class, C: student_name, D: nickname, E: year
        headers = [['student_id', 'class', 'student_name', 'nickname', 'year']]
        sheet.update('A1:E1', headers)
        print("Updated headers to: student_id, class, student_name, nickname, year")
        
        # 2. Clear existing Named Ranges to avoid conflicts
        named_ranges_response = spreadsheet.fetch_sheet_metadata()
        if 'namedRanges' in named_ranges_response:
            delete_requests = []
            for nr in named_ranges_response['namedRanges']:
                delete_requests.append({"deleteNamedRange": {"namedRangeId": nr['namedRangeId']}})
            if delete_requests:
                spreadsheet.batch_update({"requests": delete_requests})
                print("Cleared existing named ranges.")

        # 3. Create new Named Ranges
        cols = ['student_id', 'class', 'student_name', 'nickname', 'year']
        add_nr_requests = []
        for i, name in enumerate(cols):
            add_nr_requests.append({
                "addNamedRange": {
                    "namedRange": {
                        "name": name,
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": 0,
                            "endRowIndex": 1000,
                            "startColumnIndex": i,
                            "endColumnIndex": i + 1
                        }
                    }
                }
            })
        spreadsheet.batch_update({"requests": add_nr_requests})
        print("Created new named ranges for all columns.")
        
        # 4. Move Data Validation for 'year' (now Column E, index 4)
        # Clear old validation first (on old column D)
        clear_val = {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet.id,
                    "startRowIndex": 1,
                    "endRowIndex": 1000,
                    "startColumnIndex": 3,
                    "endColumnIndex": 4
                }
            }
        }
        # Set new validation on column E
        set_val = {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet.id,
                    "startRowIndex": 1,
                    "endRowIndex": 1000,
                    "startColumnIndex": 4,
                    "endColumnIndex": 5
                },
                "rule": {
                    "condition": {
                        "type": "NUMBER_BETWEEN",
                        "values": [{"userEnteredValue": "2000"}, {"userEnteredValue": "2100"}]
                    },
                    "strict": True,
                    "showCustomUi": True
                }
            }
        }
        spreadsheet.batch_update({"requests": [clear_val, set_val]})
        print("Moved year validation to column E.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    restructure_database()
