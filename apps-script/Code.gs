/**
 * Stripped Gradebook - Headless API for GitHub Pages
 * Version 1.0.7 - JSONP Support
 */

const ADMIN_PASSWORD = "12345";
let global_callback = null;

function doGet(e) {
  global_callback = e.parameter.callback;
  const action = e.parameter.action;
  const year = e.parameter.year;
  const pwd = e.parameter.pwd;

  // 1. Explicit Password Check Action
  if (action === "check") {
    const isValid = (pwd === ADMIN_PASSWORD);
    return createResponse({ success: isValid, message: isValid ? "Authorized" : "Invalid Password" });
  }

  // 2. Security Gate for other actions
  if (pwd !== ADMIN_PASSWORD) {
    return createResponse({ success: false, error: "Unauthorized" });
  }

  // 3. Action Routing
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

    if (action === "bulk_upsert") {
      const sheetName = e.parameter.sheet;
      const payload = JSON.parse(e.parameter.payload);
      const result = bulkUpsert(sheetName, payload);
      return createResponse({ success: true, message: result });
    }

    return createResponse({ success: false, error: "Unknown Action: " + action });
  } catch (err) {
    return createResponse({ success: false, error: err.message });
  }
}

function createResponse(obj) {
  const json = JSON.stringify(obj);
  if (global_callback) {
    return ContentService.createTextOutput(global_callback + "(" + json + ")")
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(json)
    .setMimeType(ContentService.MimeType.JSON);
}

function getAdminData(year) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = ["admin_settings", "admin_term_dates", "admin_holidays", "admin_students", "admin_classes", "admin_grading_policies", "admin_red_marks", "admin_cefr_lookup"];
  let data = {};

  sheets.forEach(name => {
    const sheet = ss.getSheetByName(name);
    if (!sheet) return;
    const range = sheet.getDataRange();
    const values = range.getDisplayValues();
    if (values.length < 1) return;
    
    const headers = values[0];
    const rows = values.slice(1);
    const yearIdx = headers.indexOf('year');
    
    data[name] = {
      headers: headers,
      rows: rows.filter(row => (yearIdx === -1 || !year) ? true : String(row[yearIdx]) === String(year))
                .map(row => row.map(cell => cell === null || cell === undefined ? "" : cell.toString()))
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

function bulkUpsert(sheetName, dataArray) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  const values = sheet.getDataRange().getValues();
  const headers = values[0];
  const yearIdx = headers.indexOf('year');
  const existingMap = {};
  for (let i = 1; i < values.length; i++) {
    const key = String(values[i][0]) + (yearIdx !== -1 ? String(values[i][yearIdx]) : "");
    existingMap[key] = i + 1;
  }
  dataArray.forEach(dataObject => {
    const newRow = headers.map(h => dataObject[h] || "");
    const lookupKey = String(newRow[0]) + (yearIdx !== -1 ? String(dataObject['year']) : "");
    if (existingMap[lookupKey]) sheet.getRange(existingMap[lookupKey], 1, 1, newRow.length).setValues([newRow]);
    else sheet.appendRow(newRow);
  });
  return "Processed " + dataArray.length + " records.";
}
