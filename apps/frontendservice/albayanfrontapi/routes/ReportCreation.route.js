import express from "express";
import { validateSchemas } from "../middlewares/schemaValidator.middleware.js";
import {
  createReport,
  getReportByRequestById,
  getAllReportCreationRequests,
  deleteReportRequest,
} from "../controllers/ReportCreation.controller.js";
import {
  uuidSchema,
  reportDataSchema,
  writerDataSchema,
} from "../schemas/reports.schema.js";
const ReportCreationRoute = express.Router();

ReportCreationRoute.post(
  "/reports/:reportDefinitionId/issue",
  validateSchemas(reportDataSchema, "body"),
  createReport
);

ReportCreationRoute.get(
  "/reports/:reportDefinitionId/issue",
  validateSchemas(uuidSchema, "param"),
  getAllReportCreationRequests
);

ReportCreationRoute.get(
  "/reports/:reportDefinitionId/issue/:report_request_id",
  validateSchemas(uuidSchema, "param"),
  getReportByRequestById
);
ReportCreationRoute.delete(
  "/reports/:reportDefinitionId/issue/:report_request_id",
  validateSchemas(uuidSchema, "param"),
  deleteReportRequest
);
export { ReportCreationRoute };
