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
} from "../schemas/reports.schema.js";
const ReportsDefinitionRouter = express.Router();

ReportsDefinitionRouter.post(
  "/reports",
  upload.single("file"),
  validateSchemas(reportDefinitionSchema, "body"),
  createReportDefinition
);
ReportsDefinitionRouter.get("/reports", getAllReportDefinitions);
ReportsDefinitionRouter.get(
  "/reports/:reportDefinitionId",
  validateSchemas(uuidSchema, "params"),
  getReportDefinitionById
);
ReportsDefinitionRouter.delete(
  "/reports/:reportDefinitionId",
  validateSchemas(uuidSchema, "params"),
  deleteReportDefinition
);
ReportsDefinitionRouter.patch(
  "/reports/:reportDefinitionId",
  upload.single("file"),
  validateSchemas(uuidSchema, "params"),
  validateSchemas(reportDefinitionSchema, "body"),
  updateReportDefinitionById
);
export { ReportsDefinitionRouter };
