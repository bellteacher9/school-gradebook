# Skill: Managing Google Sheets

## Metadata
- **Name:** managing-google-sheets
- **Description:** Automates interactions with the Stripped Gradebook spreadsheet using service account authentication.
- **Project:** Stripped Gradebook
- **Status:** Active

## Instructions
- Use `gsheets_connector.py` as a base for any sheet-level operations.
- Prefer deterministic Python scripts for all CRUD operations on the spreadsheet.
- Authentication is handled via the service account: `grading-app-dev@bell-474807.iam.gserviceaccount.com`.
- **Primary Spreadsheet:** `1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE`

## Resources
- **Location:** `skills/managing-google-sheets/`
- **Connector Script:** `gsheets_connector.py`
- **Spreadsheet URL:** [Google Sheet](https://docs.google.com/spreadsheets/d/1IJelEEGo4CnO24qGjAzaxg_fM0OhWlAB2o1mpfcueXE/edit)

## Hook Context
The skill can be used to inject current spreadsheet data into future sessions. 
- `_database` sheet data should be treated as the source of truth for all calculations.
