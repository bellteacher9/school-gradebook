# Stripped Gradebook - Project Context

## Project Overview
A multi-teacher gradebook system built on Google Sheets, designed to centralize data entry while providing isolated views for individual teachers. The system uses dynamic filter views for input, synchronizes data through receptacle sheets to a central database, and generates professional reports using Typst templates.

## Architecture
- **Frontend/Input:** 
    - **Teacher Views:** Google Sheets using Dynamic Filter Views.
    - **Admin Panel:** Hosted on GitHub Pages ([https://bellteacher9.github.io/school-gradebook/](https://bellteacher9.github.io/school-gradebook/)).
- **Backend/Storage:** Google Sheets acting as receptacle sheets and a central `_database` sheet.
- **Headless API:** Google Apps Script serving as a JSONP-enabled API for cross-origin communication between GitHub Pages and Google Sheets.
- **Reporting:** Typst-based templating for generating printed reports from database records.

## Core Functions
1.  **Grade Entry:** Capturing student performance data (Midterms, Finals, CA).
2.  **Attendance:** Tracking student presence, lates, and absences with automated percentage calculation.
3.  **Red Marks:** Flagging performance or behavioral concerns with a transaction-log "catcher".
4.  **Reports:** Generating formatted student reports via Typst.
5.  **Statistics:** Aggregating data for administrative insights.

## Administrative Structure
The system is managed through year-specific administrative sheets:
- `admin_settings`: Global variables.
- `admin_term_dates`: Start and end dates for academic terms.
- `admin_holidays`: Exclusion dates for attendance calculations.
- `admin_students`: Definitive student roster (supports bulk CSV upload).
- `admin_classes`: Mapping students to teachers and courses.
- `admin_grading_policies`: Weighting and passing thresholds.
- `admin_cefr_lookup`: Numeric to letter conversion for CEFR levels.

## Resources
- **Primary Spreadsheet:** [Google Sheet](https://docs.google.com/spreadsheets/d/1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE/edit)
- **Service Account:** `grading-app-dev@bell-474807.iam.gserviceaccount.com`
- **Credentials:** Located in `.credentials/bell-474807-7b515f4c9f88.json`
- **GitHub Repository:** [https://github.com/bellteacher9/school-gradebook](https://github.com/bellteacher9/school-gradebook)

## Spreadsheet Interaction Specs
- **Spreadsheet ID:** `1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE`
- **Auth Method:** 
    - **Local Python:** Service Account via `gspread`.
    - **Web App:** Google Apps Script Web App (JSONP enabled).
- **Primary Tool:** Always use the `managing-google-sheets` skill.
- **Communication Pattern:** Use JSONP to bypass browser CORS blocks when talking to the Apps Script API.

## Development Guidelines
- **Skills-Based Architecture:** Follow the modular filesystem-based skill structure defined in `skills/`.
- **Headless API Consistency:** Always update the Apps Script deployment when changing backend logic to ensure the frontend can communicate.
- **Hard Refresh Mandate:** Since GitHub Pages and Apps Script cache aggressively, always use `Ctrl + F5` to verify changes.
- **Year-Based Integrity:** Every administrative setting MUST be tied to an academic year to preserve historical data.

## Skills
- `managing-google-sheets`: Located in `skills/managing-google-sheets/`.
- `building-apps-script-interfaces`: Located in `skills/building-apps-script-interfaces/`.

## Key Files
- `GEMINI.md`: This context file.
- `knowledge-base/table_schema.json`: Definitive schema for all database and admin tables.
- `docs/index.html`: Standalone frontend for the Admin Panel.
- `apps-script/Code.gs`: Server-side API logic.
- `.credentials/`: Contains Google Cloud service account keys and GitHub tokens.
