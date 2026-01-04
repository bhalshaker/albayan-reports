import express from "express";
import { upload } from "../middlewares/upload.middleware.js";
import { validateSchemas } from "../middlewares/schemaValidator.middleware.js";
import {
  createReportDefinition,
  deleteReportDefinition,
  getAllReportDefinitions,
  getReportDefinitionById,
  updateReportDefinitionById,
} from "../controllers/ReportDefinition.controller.js";
import {
  uuidSchema,
  reportDefinitionSchema,
  writerDataSchema,
} from "../schemas/reports.schema.js";

// Define the router
const ReportsDefinitionRouter = express.Router();
// Define create report definition route
ReportsDefinitionRouter.post(
  "/reports", // Route path
  upload.single("file"), // Middleware to handle file upload
  validateSchemas(reportDefinitionSchema, "body"), // Validate request body
  createReportDefinition // Controller to handle creation
);
// Define get all report definitions route
ReportsDefinitionRouter.get(
  "/reports", //Route Path
  getAllReportDefinitions //Controller to get all report definitions
);
// Define get report definition by ID route
ReportsDefinitionRouter.get(
  "/reports/:reportDefinitionId", // Route Path
  validateSchemas(uuidSchema, "params"), // Validate request params
  getReportDefinitionById // Controller to get report definition by ID
);
// Define delete report definition route
ReportsDefinitionRouter.delete(
  "/reports/:reportDefinitionId", // Route Path
  validateSchemas(uuidSchema, "params"), // Validate request params
  deleteReportDefinition /// Controller to delete report definition
);
// Define update report definition route
ReportsDefinitionRouter.patch(
  "/reports/:reportDefinitionId", // Route Path
  upload.single("file"), // Middleware to handle file upload
  validateSchemas(uuidSchema, "params"), // Validate request params
  validateSchemas(reportDefinitionSchema, "body"), // Validate request body
  updateReportDefinitionById // Controller to update report definition
);
export { ReportsDefinitionRouter };
