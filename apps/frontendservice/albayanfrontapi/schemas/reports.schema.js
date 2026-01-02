// Schema definition for uuid validation
const uuidSchema = {
  type: "string",
  format: "uuid",
};

// Schema definition for report definition creation
const reportDefinitionSchema = {
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

// Schema definition for report data submission
const reportDataSchema = {
  type: "object",
  required: ["report_output_format", "report_data"],
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

// Schema definition for writer data used in report generation
const writerDataSchema = {
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
