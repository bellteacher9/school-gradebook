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

def fix_cefr_prefix():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet('_database')
        
        # 1. Update Header BC1
        sheet.update_cell(1, 55, 'Term_02_overall_cefr_letter')
        print("Updated cell BC1 to 'Term_02_overall_cefr_letter'")
        
        # 2. Fix Named Range
        # First, delete the old one
        named_ranges_response = spreadsheet.fetch_sheet_metadata()
        if 'namedRanges' in named_ranges_response:
            for nr in named_ranges_response['namedRanges']:
                if nr['name'] == 'Term02_overall_cefr_letter':
                    spreadsheet.batch_update({
                        "requests": [{"deleteNamedRange": {"namedRangeId": nr['namedRangeId']}}]
                    })
                    print("Deleted old named range 'Term02_overall_cefr_letter'")
                    break

        # Now add the corrected one
        spreadsheet.batch_update({
            "requests": [{
                "addNamedRange": {
                    "namedRange": {
                        "name": "Term_02_overall_cefr_letter",
                        "range": {
                            "sheetId": sheet.id,
                            "startRowIndex": 0,
                            "endRowIndex": 1000,
                            "startColumnIndex": 54,
                            "endColumnIndex": 55
                        }
                    }
                }
            }]
        })
        print("Created corrected named range 'Term_02_overall_cefr_letter'")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_cefr_prefix()
