# Skill: Building Apps Script Interfaces

## Metadata
- **Name:** building-apps-script-interfaces
- **Description:** Rapidly develops and deploys SPA (Single Page Application) web interfaces within Google Apps Script.
- **Project:** Stripped Gradebook
- **Status:** Active

## Instructions
- **Architecture:** Use a standard `Code.gs` for server functions and `Index.html` for the client.
- **Modular Templates:** Split HTML, CSS, and JS into separate `.html` files and include them using `<?!= include('filename'); ?>`.
- **Communication:** Use `google.script.run` for all server-side calls (e.g., `fetchSheetData`, `saveRowData`).
- **Standard UI Patterns:**
    - Sidebar or Top Tabs for navigation between `admin_` sheets.
    - Data tables that are dynamically populated from a JSON response.
    - Uniform "Save" and "Refresh" buttons for all admin settings.
- **Styling:** Use Vanilla CSS with a focus on high contrast (Maroon, Dark Gray, White) to match the project's dashboard.

## Resources
- **Location:** `skills/building-apps-script-interfaces/`
- **Reference Docs:** [GAS HTML Service](https://developers.google.com/apps-script/guides/html)
- **Primary Template:** `webapp_boilerplate/` (to be created)

## Hook Context
Injects common Apps Script boilerplate into the session.
- `doGet()` function for initial page load.
- `include(filename)` helper function for template inclusion.
