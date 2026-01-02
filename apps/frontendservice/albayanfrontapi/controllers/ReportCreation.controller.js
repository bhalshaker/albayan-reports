import {
  createReportService,
  deleteReportRequestService,
  getReportRequestByReportRequestIdService,
  listReportRequestsService,
} from "../services/database.js";
import errorResponse from "../utils/errorResponse.utils.js";
import { createReportFromWorker } from "../services/worker.service.js";

// Create Report Controller
const createReport = async (request, response) => {
  try {
    // Create a new report request in the database
    const createReportRecord = await createReportService(
      request.params.reportDefinitionId,
      request.body.output_format,
      request.body.report_data
    );
    // Fetch the created report from the worker service
    const createReportRequest = await createReportFromWorker(
      createReportRecord.report_request_id
    );
    // Send successful response with the created report data
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: {
        report_request_id: request.params.report_request_id,
        report_data: createReportRequest,
      },
    });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

// Get Report By Request ID Controller
const getReportByRequestById = async (request, response) => {
  try {
    // Fetch the report creation request from the database
    const reportCreationRequest =
      await getReportRequestByReportRequestIdService(
        request.params.report_request_id
      );
    // If not found, return 404 response
    if (!reportCreationRequest)
      return response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
    // Send successful response with the report creation request data
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: {
        report_request_id: request.params.report_request_id,
        report_data: reportCreationRequest,
      },
    });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

// Get All Report Creation Requests Controller
const getAllReportCreationRequests = async (request, response) => {
  try {
    // Fetch all report creation requests from the database
    const allReportCreationRequests = await listReportRequestsService();
    // Send successful response with all report creation requests
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: allReportCreationRequests,
    });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

// Delete Report Request Controller
const deleteReportRequest = async (request, response) => {
  try {
    // Delete the report request from the database
    await deleteReportRequestService(request.params.report_request_id);
    // Send successful deletion response
    return response.status(202).json({
      success: true,
      message: "successful",
      details: null,
      data: null,
    });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

export {
  createReport,
  getReportByRequestById,
  getAllReportCreationRequests,
  deleteReportRequest,
};
