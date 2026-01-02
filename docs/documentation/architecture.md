## Report Request Schema

```js
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Report Request Schema",
  "type": "object",
  "required": [
    "report_request_id",
    "report_template_id",
    "report_output_format",
    "report_data",
    "request_date",
    "update_date",
    "processing_status"
  ],
  "properties": {
    "report_request_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for the report request."
    },
    "report_template_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for the template being used."
    },
    "report_output_format": {
      "type": "string",
      "enum": [
        "PDF",
        "OPENOFFICE",
        "PDF+OPENOFFICE"
      ],
      "description": "The desired output format for the generated report."
    }
    "report_data": {
      "type": "object",
      "description": "A dictionary/object containing the actual data for the report.",
      "additionalProperties": true
    },
    "request_date":{
      "type": "string",
      "format":"date-time",
      "description":"Time stamp is in ISO 8601 format. e.g., 2025-12-20T13:33:25Z"
    },
    "update_date":{
      "type": "string",
      "format":"date-time",
      "description":"Time stamp is in ISO 8601 format. e.g., 2025-12-20T13:33:25Z"
    },
     "processing_status": {
      "type": "string",
      "enum": [
        "PENDING",
        "SUCESSFUL",
        "FAILED"
      ],
      "description": "The status of report creation."
    }
  }
}
```

## Report Template Schema

```js
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Report Template Schema",
  "type": "object",
  "required": [
    "report_template_id",
    "template_file",
    "template_file_type",
    "creation_date",
    "updated_date"
  ],
  "properties": {
    "report_template_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for the report template."
    },
    "template_file": {
      "type": "string",
      "description": "The path, URL, or base64 encoded content of the template file."
    },
    "template_file_type": {
      "type": "string",
      "enum": ["odf"],
      "description": "The file format of the template (currently restricted to ODF)."
    },
    "creation_date":{
      "type": "string",
      "format":"date-time",
      "description":"Time stamp is in ISO 8601 format. e.g., 2025-12-20T13:33:25Z"
    },
    "updated_date":{
      "type": "string",
      "format":"date-time",
      "description":"Time stamp is in ISO 8601 format. e.g., 2025-12-20T13:33:25Z"
    }
  }
}
```

## Writer Data Schema

```py
instance={"writer_placeholders":[],"writer_variables":[],"writer_images":{},"writer_tables":[]}
```

```js
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Writer Data Schema",
  "type": "object",
  "required": [
    "writer_placeholders",
    "writer_variables",
    "writer_images",
    "writer_tables"
  ],
  "properties": {
    "writer_placeholders": {
      "type": "array",
      "items": {
        "type": "object",
        "patternProperties": {
          "^.*$": { "type": "string" }
        },
        "description": "An object where keys are placeholder names and values are strings."
      }
    },
    "writer_variables": {
      "type": "array",
      "items": {
        "type": "object",
        "patternProperties": {
          "^.*$": { "type": "string" }
        },
        "description": "An object where keys are variable names and values are strings."
      }
    },
    "writer_images": {
      "type": "object",
      "patternProperties": {
        "^.*$": {
          "type": "string",
          "description": "Base64 encoded image string."
        }
      }
    },
    "writer_tables": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["table_name", "content"],
        "properties": {
          "table_name": { "type": "string" },
          "content": {
            "type": "array",
            "items": {
              "type": "object",
              "patternProperties": {
                "^.*$": { "type": "string" }
              }
            }
          },
          "footer": {
            "type": "object",
            "patternProperties": {
              "^.*$": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```
