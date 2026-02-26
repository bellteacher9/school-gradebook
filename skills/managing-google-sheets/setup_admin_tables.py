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

def setup_admin_tables():
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # Define the tables and their headers
        admin_tables = {
            "admin_settings": ["Variable", "Value", "Description"],
            "admin_students": ["student_id", "student_name", "nickname", "email", "active_status"],
            "admin_classes": ["class_id", "year", "teacher_email", "course_level"],
            "admin_grading_policies": ["policy_name", "component", "weight_percentage", "min_passing_score"],
            "admin_red_marks": ["category", "trigger_threshold", "action_required"],
            "admin_cefr_lookup": ["min_score", "max_score", "cefr_letter", "cefr_number_equivalent"]
        }
        
        for sheet_name, headers in admin_tables.items():
            # Create or get the worksheet
            try:
                sheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
                print(f"Created '{sheet_name}' worksheet.")
            except gspread.exceptions.APIError as e:
                if "already exists" in str(e):
                    sheet = spreadsheet.worksheet(sheet_name)
                    print(f"Worksheet '{sheet_name}' already exists.")
                else:
                    raise e
            
            # Update headers
            sheet.update(range_name='A1', values=[headers])
            print(f"Set up headers for '{sheet_name}': {', '.join(headers)}")

        # Optional: Remove the generic 'administrator' sheet if it exists
        try:
            old_admin = spreadsheet.worksheet("administrator")
            spreadsheet.del_worksheet(old_admin)
            print("Removed the legacy 'administrator' worksheet.")
        except gspread.exceptions.WorksheetNotFound:
            pass

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_admin_tables()
