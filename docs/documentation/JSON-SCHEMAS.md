## Report Request Schema

```js
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Report Request Schema",
  "type": "object",
  "required": [
    "report_request_id",
    "report_template_id",
    "report_template_version",
    "report_output_format",
    "report_data"
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
    "report_template_version": {
      "type": "integer",
      "minimum": 1,
      "description": "The version number of the report template."
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
    "report_template_version",
    "template_file",
    "template_file_type",
    "template_data_definition"
  ],
  "properties": {
    "report_template_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for the report template."
    },
    "report_template_version": {
      "type": "integer",
      "description": "The version number of the template."
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
    "template_data_definition": {
      "type": "object",
      "description": "A schema or dictionary defining the structure of the data this template expects.",
      "additionalProperties": true
    }
  }
}
```

## Writer Data Schema

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
