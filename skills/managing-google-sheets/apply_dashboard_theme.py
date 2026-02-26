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

def apply_dashboard_theme():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        dashboard = spreadsheet.worksheet("dashboard")
        
        # Colors (0.0 to 1.0 range)
        MAROON = {"red": 0.5, "green": 0.0, "blue": 0.0}
        DARK_GRAY = {"red": 0.26, "green": 0.26, "blue": 0.26}
        WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}

        body = {
            "requests": [
                # 1. Header Area (Rows 1-2): Maroon background
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": dashboard.id,
                            "startRowIndex": 0, "endRowIndex": 2,
                            "startColumnIndex": 0, "endColumnIndex": 10
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": MAROON,
                                "textFormat": {"foregroundColor": WHITE, "bold": True}
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat)"
                    }
                },
                # 2. Headline 1: Larger font
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": dashboard.id,
                            "startRowIndex": 0, "endRowIndex": 1,
                            "startColumnIndex": 2, "endColumnIndex": 3
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {"fontSize": 16}
                            }
                        },
                        "fields": "userEnteredFormat.textFormat.fontSize"
                    }
                },
                # 3. Prompt (A4): Dark Gray text
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": dashboard.id,
                            "startRowIndex": 3, "endRowIndex": 4,
                            "startColumnIndex": 0, "endColumnIndex": 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {"foregroundColor": DARK_GRAY, "bold": True}
                            }
                        },
                        "fields": "userEnteredFormat.textFormat.foregroundColor,userEnteredFormat.textFormat.bold"
                    }
                },
                # 4. Selection Cell (B4): Maroon Border
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": dashboard.id,
                            "startRowIndex": 3, "endRowIndex": 4,
                            "startColumnIndex": 1, "endColumnIndex": 2
                        },
                        "top": {"style": "SOLID_MEDIUM", "color": MAROON},
                        "bottom": {"style": "SOLID_MEDIUM", "color": MAROON},
                        "left": {"style": "SOLID_MEDIUM", "color": MAROON},
                        "right": {"style": "SOLID_MEDIUM", "color": MAROON}
                    }
                }
            ]
        }
        spreadsheet.batch_update(body)
        print("Applied maroon, dark gray, and white theme to the dashboard.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    apply_dashboard_theme()
