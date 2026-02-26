/**
 * Stripped Gradebook - Headless API for GitHub Pages
 */

const ADMIN_PASSWORD = "12345";

function doGet(e) {
  const action = e.parameter.action;
  const year = e.parameter.year;
  const pwd = e.parameter.pwd;

  // 1. Password Verification
  if (pwd !== ADMIN_PASSWORD && action !== "check") {
    return createResponse({ success: false, error: "Unauthorized" });
  }

  // 2. Action Routing
  try {
    if (action === "fetch") {
      const data = getAdminData(year);
      return createResponse({ success: true, data: data });
    }
    
    if (action === "upsert") {
      const sheetName = e.parameter.sheet;
      const payload = JSON.parse(e.parameter.payload);
      const result = upsertAdminData(sheetName, payload);
      return createResponse({ success: true, message: result });
    }

    return createResponse({ success: true, message: "API Active" });
  } catch (err) {
    return createResponse({ success: false, error: err.message });
  }
}

function createResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Re-using existing data functions
 */
function getAdminData(year) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = ["admin_settings", "admin_term_dates", "admin_holidays", "admin_students", "admin_classes", "admin_grading_policies", "admin_red_marks", "admin_cefr_lookup"];
  let data = {};

  sheets.forEach(name => {
    const sheet = ss.getSheetByName(name);
    if (!sheet) return;
    const values = sheet.getDataRange().getValues();
    if (values.length < 1) return;
    
    const headers = values[0];
    const rows = values.slice(1);
    const yearIdx = headers.indexOf('year');
    
    data[name] = {
      headers: headers,
      rows: rows.filter(row => (yearIdx === -1 || !year) ? true : String(row[yearIdx]) === String(year))
    };
  });
  return data;
}

function upsertAdminData(sheetName, dataObject) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  const values = sheet.getDataRange().getValues();
  const headers = values[0];
  const newRow = headers.map(h => dataObject[h] || "");
  
  let rowIndex = -1;
  const yearIdx = headers.indexOf('year');

  for (let i = 1; i < values.length; i++) {
    const matchKey = String(values[i][0]) === String(newRow[0]);
    const matchYear = (yearIdx === -1) || String(values[i][yearIdx]) === String(dataObject['year']);
    if (matchKey && matchYear) { rowIndex = i + 1; break; }
  }

  if (rowIndex !== -1) {
    sheet.getRange(rowIndex, 1, 1, newRow.length).setValues([newRow]);
    return "Updated";
  } else {
    sheet.appendRow(newRow);
    return "Created";
  }
}
