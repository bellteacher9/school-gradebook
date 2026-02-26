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
SPREADSHEET_ID = '1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE'

def list_named_ranges():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        metadata = spreadsheet.fetch_sheet_metadata()
        named_ranges = metadata.get('namedRanges', [])
        
        # Sort by startColumnIndex to see them in order
        sorted_ranges = sorted(named_ranges, key=lambda x: x['range'].get('startColumnIndex', 0))
        
        print(f"Total Named Ranges: {len(sorted_ranges)}")
        for nr in sorted_ranges:
            name = nr['name']
            r = nr['range']
            col_start = r.get('startColumnIndex', 0)
            print(f"Col {col_start}: {name}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    list_named_ranges()
