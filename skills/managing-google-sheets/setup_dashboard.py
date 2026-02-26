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

def setup_dashboard():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # 1. Create the 'dashboard' worksheet
        try:
            dashboard = spreadsheet.add_worksheet(title="dashboard", rows="30", cols="10")
            print("Created 'dashboard' worksheet.")
        except gspread.exceptions.APIError as e:
            if "already exists" in str(e):
                dashboard = spreadsheet.worksheet("dashboard")
                print("Worksheet 'dashboard' already exists.")
            else:
                raise e

        # 2. Set up the Layout
        # We'll use formatting to create the 'decks'
        
        # Logo Placeholder in A1:B2 (merged area)
        dashboard.update('A1', [['[LOGO]']])
        
        # Headline Decks
        # Deck 1: C1
        # Deck 2: C2
        dashboard.update('C1:C2', [['Cambridge English Language Program'], ['Mathayom, M1-M3, Regular Program']])
        
        # Interaction Prompt
        dashboard.update('A4', [['Choose a class to get started:']])
        
        # Placeholder for Dropdown (B4)
        dashboard.update('B4', [['---Select Class---']])
        
        # Formatting (best effort via batch_update)
        # Bold headlines and merge logo area
        body = {
            "requests": [
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": dashboard.id,
                            "startRowIndex": 0, "endRowIndex": 2,
                            "startColumnIndex": 0, "endColumnIndex": 2
                        },
                        "mergeType": "MERGE_ALL"
                    }
                },
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": dashboard.id,
                            "startRowIndex": 0, "endRowIndex": 2,
                            "startColumnIndex": 2, "endColumnIndex": 3
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {"bold": True, "fontSize": 14}
                            }
                        },
                        "fields": "userEnteredFormat.textFormat"
                    }
                }
            ]
        }
        spreadsheet.batch_update(body)
        print("Set up dashboard layout and formatting.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_dashboard()
