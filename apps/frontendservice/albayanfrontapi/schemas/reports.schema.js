const uuidSchema = {
  type: "string",
  format: "uuid",
};

const reportDefinitionSchema = {
  $schema: "https://json-schema.org/draft/2020-12/schema",
  title: "Report Template Schema",
  type: "object",
  required: ["template_file_type"],
  properties: {
    template_file_type: {
      type: "string",
      enum: ["odf"],
      description:
        "The file format of the template (currently restricted to ODF).",
    },
  },
};

const reportDataSchema = {
  $schema: "https://json-schema.org/draft/2020-12/schema",
  title: "Report Request Schema",
  type: "object",
  required: [
    "report_output_format",
    "report_data",
    "request_date",
    "update_date",
    "processing_status",
  ],
  properties: {
    report_output_format: {
      type: "string",
      enum: ["PDF", "OPENOFFICE", "PDF+OPENOFFICE"],
      description: "The desired output format for the generated report.",
    },
    report_data: {
      type: "object",
      description:
        "A dictionary/object containing the actual data for the report.",
      additionalProperties: true,
    },
  },
};

const writerDataSchema = {
  $schema: "https://json-schema.org/draft/2020-12/schema",
  title: "Writer Data Schema",
  type: "object",
  required: [
    "writer_placeholders",
    "writer_variables",
    "writer_images",
    "writer_tables",
  ],
  properties: {
    writer_placeholders: {
      type: "array",
      items: {
        type: "object",
        patternProperties: {
          "^.*$": { type: "string" },
        },
        description:
          "An object where keys are placeholder names and values are strings.",
      },
    },
    writer_variables: {
      type: "array",
      items: {
        type: "object",
        patternProperties: {
          "^.*$": { type: "string" },
        },
        description:
          "An object where keys are variable names and values are strings.",
      },
    },
    writer_images: {
      type: "object",
      patternProperties: {
        "^.*$": {
          type: "string",
          description: "Base64 encoded image string.",
        },
      },
    },
    writer_tables: {
      type: "array",
      items: {
        type: "object",
        required: ["table_name", "content"],
        properties: {
          table_name: { type: "string" },
          content: {
            type: "array",
            items: {
              type: "object",
              patternProperties: {
                "^.*$": { type: "string" },
              },
            },
          },
          footer: {
            type: "object",
            patternProperties: {
              "^.*$": { type: "string" },
            },
          },
        },
      },
    },
  },
};

export {
  uuidSchema,
  reportDefinitionSchema,
  reportDataSchema,
  writerDataSchema,
};
