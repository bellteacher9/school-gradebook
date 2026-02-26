# Stripped Gradebook - Project Context

## Project Overview
A multi-teacher gradebook system built on Google Sheets, designed to centralize data entry while providing isolated views for individual teachers. The system uses dynamic filter views for input, synchronizes data through receptacle sheets to a central database, and generates professional reports using Typst templates.

## Architecture
- **Frontend/Input:** Google Sheets using Dynamic Filter Views for concurrent teacher access.
- **Backend/Storage:** Google Sheets acting as receptacle sheets and a central `_database` sheet.
- **Management:** Google Apps Script Web Interface for administrator control of variables and system configuration.
- **Reporting:** Typst-based templating for generating printed reports from database records.

## Core Functions
1.  **Grade Entry:** Capturing student performance data.
2.  **Attendance:** Tracking student presence and participation.
3.  **Red Marks:** Flagging performance or behavioral concerns.
4.  **Reports:** Generating formatted student reports via Typst.
5.  **Statistics:** Aggregating data for administrative insights.

## Resources
- **Primary Spreadsheet:** [Google Sheet](https://docs.google.com/spreadsheets/d/1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE/edit)
- **Service Account:** `grading-app-dev@bell-474807.iam.gserviceaccount.com`
- **Credentials:** Located in `.credentials/bell-474807-7b515f4c9f88.json`

## Spreadsheet Interaction Specs
- **Spreadsheet ID:** `1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE`
- **Auth Method:** Service Account via `gspread` Python library.
- **Library Requirements:** `gspread`, `google-auth`.
- **Primary Tool:** Always use the `managing-google-sheets` skill located in `skills/managing-google-sheets/`.
- **Operational Rule:** Prefer writing and executing Python scripts (e.g., `gsheets_connector.py`) over manual API calls to ensure deterministic results.
- **Critical Sheets:**
    - `_database`: The single source of truth for the system.

## Development Guidelines
- **Skills-Based Architecture:** Follow the modular filesystem-based skill structure defined in `skills/`.
- **Managing Google Sheets:** Use the `managing-google-sheets` skill for all spreadsheet interactions.
- **Data Flow:** All data entered via filter views must flow through designated "receptacle" sheets before being committed to the central `_database`.
- **Admin Control:** System variables (terms, subjects, grading scales) are managed exclusively through the Apps Script web interface.
- **Security:** Use the provided service account for any external scripts or API interactions.

## Skills
- `managing-google-sheets`: Located in `skills/managing-google-sheets/`.
- `building-apps-script-interfaces`: Located in `skills/building-apps-script-interfaces/`.

## Key Files
- `GEMINI.md`: This context file.
- `knowledge-base/table_schema.json`: Definitive schema for all database tables.
- `.credentials/`: Contains Google Cloud service account keys.
- `images/`: Project assets including `logo2.jpg`.
