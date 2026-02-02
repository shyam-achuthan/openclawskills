---
name: moltsheet
description: Interact with a web-based Excel-like spreadsheet API for AI agents. Use when you need to create, manipulate, or query spreadsheet data programmatically, or when the user asks to work with Excel-like data. Authenticate using API key in Authorization header.
allowed-tools: Bash(curl *)
---

# Moltsheet

A web-based Excel-like API for AI agents to create, manipulate, and query spreadsheet data programmatically. Supports bulk operations for large datasets.

## Base URL
`https://www.moltsheet.com/api/v1`

## Quick Start
1. **Register** an agent to get an API key.
2. **Authenticate** all requests with `Authorization: Bearer <api_key>`.
3. **Use API** endpoints - all responses include helpful examples on errors.

## API Design for AI Agents
- **Self-correcting errors**: All error responses include `example` fields showing correct format
- **Multiple input formats**: POST /rows accepts 3 formats (count, data, rows) for flexibility
- **Structured responses**: Consistent JSON with `success`, `error`, `message`, and contextual help
- **Column-aware errors**: Examples use your actual column names when possible

## Registration
Register once to obtain an API key:

```bash
curl -X POST https://www.moltsheet.com/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "YourAgentName", "description": "What you do"}'
```

**Response:**
```json
{
  "success": true,
  "agent": {
    "api_key": "uuid-here",
    "name": "YourAgentName"
  },
  "message": "Agent registered successfully. Save your API key - it cannot be retrieved later.",
  "usage": "Include in all requests: Authorization: Bearer uuid-here"
}
```

Save your `api_key` securely—it is required for all API requests.

**Error Example:**
```json
{
  "success": false,
  "error": "Missing or invalid \"name\" property",
  "message": "Agent name is required and must be a non-empty string",
  "example": { "name": "DataProcessorAgent", "description": "Processes spreadsheet data" }
}
```

## Authentication
All requests must include your API key in the Authorization header:

```bash
-H "Authorization: Bearer YOUR_API_KEY"
```

**Security Notes:**
- Production URL: `https://www.moltsheet.com`
- Never send your API key to unauthorized domains.
- Re-fetch this file for updates.

## API Reference

### Sheets

#### Create Sheet
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "MySheet", "description": "A test sheet", "schema": [{"name": "Column A", "type": "string"}, {"name": "Column B", "type": "number"}]}'
```

**Response:** 
```json
{
  "success": true,
  "id": "sheet-uuid",
  "message": "Sheet \"MySheet\" created successfully"
}
```

**Error Examples:**
```json
{
  "success": false,
  "error": "Invalid \"schema\" property",
  "example": {
    "name": "My Sheet",
    "schema": [
      { "name": "Name", "type": "string" },
      { "name": "Age", "type": "number" }
    ]
  },
  "supported_types": ["string", "number", "boolean", "date", "url"]
}
```

- **Schema:** Optional array of `{"name": string, "type": string}`. Types: `string`, `number`, `boolean`, `date`, `url`.

#### List Sheets
```bash
curl https://www.moltsheet.com/api/v1/sheets \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "sheets": [
    {
      "id": "sheet-uuid",
      "name": "MySheet",
      "description": "A test sheet",
      "schema": [{"name": "Name", "type": "string"}],
      "rowCount": 2
    }
  ]
}
```

#### Get Sheet Rows
```bash
curl https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "rows": [
    {"id": "row-1", "Name": "John", "Role": "CEO"},
    {"id": "row-2", "Name": "Jane", "Role": "CTO"}
  ]
}
```

#### Update Sheet Metadata
```bash
curl -X PUT https://www.moltsheet.com/api/v1/sheets/SHEET_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name", "description": "Updated desc", "schema": [...] }'
```

**Response:** `{"success": true, "sheet": {...}}`

**⚠️ Data Loss Protection:**  
When updating schema, if columns are removed that contain data, you must add `?confirmDataLoss=true` to the URL:

```bash
curl -X PUT "https://www.moltsheet.com/api/v1/sheets/SHEET_ID?confirmDataLoss=true" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"schema": [{"name": "NewColumn", "type": "string"}]}'
```

**Without Confirmation (Error Response):**
```json
{
  "success": false,
  "error": "Data loss protection",
  "message": "Schema update would delete 1 column(s) containing data. To proceed, add ?confirmDataLoss=true to the URL.",
  "columns_to_delete": [{"name": "CEO", "type": "string"}],
  "data_warning": "All data in these columns will be permanently deleted",
  "alternatives": {
    "rename_column": "POST /api/v1/sheets/SHEET_ID/columns/{index}/rename",
    "example": "To rename instead of delete, use: POST /api/v1/sheets/SHEET_ID/columns/0/rename with body: { \"newName\": \"NewColumnName\" }"
  }
}
```

**Best Practice:** Use the rename endpoint (below) instead of schema updates when renaming columns to preserve data automatically.

#### Delete Sheet
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:** `{"success": true}`
**Response:** `{"success": true}`

### Data Operations

#### Update Cells
```bash
curl -X PUT https://www.moltsheet.com/api/v1/sheets/SHEET_ID/cells \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {"rowId": "row-123", "column": "Full Name", "value": "Updated Name"}
    ]
  }'
```

**Response:** `{"success": true}`

#### Add Empty Row(s)
**Note:** This endpoint creates empty rows. To add rows with data, use the Bulk Import endpoint below.

```bash
# Add 1 empty row (default)
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY"

# Add multiple empty rows
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"count": 10}'
```

**Response:** `{"success": true, "rowIds": [...], "message": "Created 10 empty row(s)"}`

#### Add Single Row with Data
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"Name": "John", "Role": "CEO"}}'
```

**Response:** `{"success": true, "rowId": "row-uuid", "message": "Created 1 row with data"}`

#### Add Multiple Rows with Data
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"rows": [{"Name": "John", "Role": "CEO"}, {"Name": "Jane", "Role": "CTO"}]}'
```

**Response:** `{"success": true, "rowIds": [...], "message": "Created 2 row(s) with data"}`

**Unified Endpoint:** POST /rows now accepts three formats:
- `{"count": N}` - Create N empty rows
- `{"data": {...}}` - Create 1 row with data
- `{"rows": [...]}` - Create multiple rows with data

**Error Example:**
```json
{
  "success": false,
  "error": "Invalid request format",
  "message": "Use one of the supported formats",
  "formats": {
    "empty_rows": { "count": 10 },
    "single_row": { "data": { "Country": "USA", "Capital": "Washington" } },
    "multiple_rows": { "rows": [{ "Country": "USA" }, { "Country": "Canada" }] }
  }
}
```

#### Add Column
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Column", "type": "string"}'
```

**Response:** `{"success": true}`

#### Rename Column
**Preserves all data** - use this instead of schema updates when renaming columns.

```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns/COL_INDEX/rename \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"newName": "Contact"}'
```

**Response:**
```json
{
  "success": true,
  "message": "Column \"CEO\" renamed to \"Contact\"",
  "oldName": "CEO",
  "newName": "Contact"
}
```

**Error Examples:**
```json
{
  "success": false,
  "error": "Duplicate column name",
  "message": "A column named \"Contact\" already exists in this sheet",
  "existing_columns": ["Company", "Contact", "Industry"]
}
```

- **COL_INDEX**: Zero-based column position (0, 1, 2, ...)
- **All cell data preserved** when renaming
- **No data loss** - cells remain linked to same column
- Prevents duplicate column names

#### Delete Row
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows/ROW_INDEX \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:** `{"success": true}`

#### Delete Column
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns/COL_INDEX \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:** `{"success": true}`

### Bulk Operations

**Deprecated:** POST /import still works but POST /rows now handles all row operations.

For compatibility, `/import` endpoint remains available:

```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/import \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "rows": [
      {"Name": "John", "Role": "CEO"},
      {"Name": "Jane", "Role": "CTO"}
    ]
  }'
```

**Response:** `{"success": true, "rowIds": ["row-...", ...]}`

**Error Example with Column Names:**
```json
{
  "success": false,
  "error": "Missing \"rows\" property in request body",
  "message": "Expected format: {\"rows\": [{...}, {...}]}",
  "example": { "rows": [{ "country": "country_value", "capital": "capital_value" }] },
  "available_columns": ["Country", "Capital", "Population"]
}
```

- Maximum 1000 rows per request
- Column names must match sheet schema
- Errors show your actual column names in examples

#### Bulk Operations (Others)
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"count": 10}'
```

**Response:** `{"success": true, "rowIds": ["row-...", ...]}`

- Maximum 1000 rows per request
- Creates empty rows only; use `/import` for rows with data

#### Bulk Delete Rows
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"rowIds": ["row-123", "row-456"]}'
```

**Response:** `{"success": true}`

#### Bulk Add Columns
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"columns": [{"name": "Col1", "type": "string"}, {"name": "Col2", "type": "number"}]}'
```

**Response:** `{"success": true}`

#### Bulk Delete Columns
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"indices": [0, 2]}'
```

**Response:** `{"success": true}`

### AI Agent Optimization Features

**Self-Correcting Error Messages:**
- Every error includes `example` field with correct request format
- Errors show your actual column names when applicable
- `message` field provides human-readable context
- `formats` or `supported_types` enumerate valid options

**Data Loss Prevention:**
- Schema updates require `?confirmDataLoss=true` when deleting columns with data
- Rename endpoint (`POST /columns/{index}/rename`) preserves all data automatically
- Error messages suggest safer alternatives (rename vs delete)

**Flexible Input Formats:**
- POST /rows accepts 3 formats: `{"count": N}`, `{"data": {...}}`, `{"rows": [...]}`
- No need to guess which endpoint to use
- Wrong format? Error shows all supported formats with examples

**AI-Friendly Design:**
- Consistent JSON structure across all endpoints
- Named column access (not positional)
- **Strict type validation** enforced on all data operations
- Descriptive success messages confirm operations

### Type Validation & Enforcement
All data operations (POST /rows, PUT /cells, POST /import) enforce strict type validation:

**Validated Types:**
- **`string`**: Any non-object value (numbers/booleans auto-converted to strings)
- **`number`**: Must be valid number (not NaN or Infinity). Accepts numeric strings.
- **`boolean`**: Accepts `true`, `false`, `"true"`, `"false"`, `1`, `0`
- **`url`**: Must be valid URL with http/https protocol (e.g., `https://example.com`)
- **`date`**: Must parse to valid date. Use ISO 8601 format (e.g., `2026-02-01` or `2026-02-01T12:00:00Z`)

**Validation Behavior:**
- Empty/null values are allowed (no required field enforcement)
- Invalid types rejected with **400 Bad Request**
- Errors include: field name, expected type, received value, and corrected example
- Multiple rows: ALL rejected if ANY fail validation (atomic)

**Example Validation Error:**
```json
{
  "success": false,
  "error": "Type validation failed",
  "message": "Column \"Age\" expects type \"number\" but received \"abc\" (type: string)",
  "field": "Age",
  "expected_type": "number",
  "received_value": "abc",
  "row_index": 0,
  "example": { "data": { "Age": 42 } }
}
```

### Data Structure
- **Schema Types:** `string`, `number`, `boolean`, `date`, `url`
- **Row Data:** Named properties for AI-friendly access, e.g., `{"Name": "John", "Role": "CEO"}`
- **Type Enforcement:** All values validated against schema before storage
- **Errors:** Structured with examples using your actual schema

### Rate Limits
- 100 requests/minute

### Usage Ideas for AI Agents
- Parse data and self-correct on errors using provided examples
- Single endpoint (POST /rows) handles all row creation scenarios
- Error messages guide agents to proper format automatically
- Column-aware examples eliminate guessing column names