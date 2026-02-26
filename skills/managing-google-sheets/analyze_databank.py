import gspread
from google.oauth2.service_account import Credentials
import sys
import os
import json

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

CREDENTIALS_PATH = os.path.join('.credentials', 'bell-474807-7b515f4c9f88.json')
# New Spreadsheet ID for analysis
DATABANK_SPREADSHEET_ID = '1A_SHHB8sje5Nc6jzNIbUQwe0PYlb1TPojYN0tbsF_sk'

def analyze_databank():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        spreadsheet = client.open_by_key(DATABANK_SPREADSHEET_ID)
        # Try to find the 'DATABANK' sheet
        try:
            sheet = spreadsheet.worksheet('DATABANK')
        except gspread.exceptions.WorksheetNotFound:
            print("Error: 'DATABANK' worksheet not found. Available sheets:")
            for s in spreadsheet.worksheets():
                print(f"- {s.title}")
            return

        headers = sheet.row_values(1)
        # Get a sample of data (first 5 rows)
        sample_data = sheet.get_all_records(head=1, default_blank=None)[:5]
        
        analysis = {
            "spreadsheet_title": spreadsheet.title,
            "headers": headers,
            "column_count": len(headers),
            "sample_rows": sample_data
        }
        
        print(json.dumps(analysis, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    analyze_databank()
