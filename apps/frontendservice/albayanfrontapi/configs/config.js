import dotenv from "dotenv";

// Load environment variables
dotenv.config();
// config dictionary with populated values from OS ENV
const config = {
  PORT: parseInt(process.env.PORT, 10) || 3000,
  NODE_ENV: process.env.NODE_ENV || "development",
  AWS_REGION: process.env.AWS_REGION,
  DYNAMODB_ENDPOINT: process.env.DYNAMODB_ENDPOINT,
  DEFINITION_TABLE: process.env.DEFINITION_TABLE || "reports_definition",
  PROCESSING_TABLE: process.env.PROCESSING_TABLE || "reports_processing",
  WORKER_URL: process.env.WORKER_URL || "http://localhost:8000",
  UPLOAD_FOLDER: process.env.UPLOAD_FOLDER,
  REPORT_OUTPUT_FOLDER: process.env.REPORT_OUTPUT_FOLDER || "/tmp/output",
};

// Export config dictionary
export { config };
