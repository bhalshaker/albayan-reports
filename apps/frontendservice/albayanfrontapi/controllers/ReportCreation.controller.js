import {
  createReportService,
  deleteReportRequestService,
  getReportRequestByReportRequestIdService,
  listReportRequestsService,
} from "../services/database.js";
import errorResponse from "../utils/errorResponse.utils.js";
import { createReportFromWorker } from "../services/worker.service.js";

const createReport = async (request, response) => {
  try {
    const createReportRecord = await createReportService(
      request.params.reportDefinitionId,
      request.body.output_format,
      request.body.report_data
    );
    const createReportRequest = await createReportFromWorker(
      createReportRecord.report_request_id
    );
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
    return await errorResponse(error);
  }
};

const getReportByRequestById = async (request, response) => {
  try {
    const reportCreationRequest =
      await getReportRequestByReportRequestIdService(
        request.params.report_request_id
      );
    if (!reportCreationRequest)
      return response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
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
    return await errorResponse(error);
  }
};

const getAllReportCreationRequests = async (request, response) => {
  try {
    const allReportCreationRequests = await listReportRequestsService();
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: allReportCreationRequests,
    });
  } catch (error) {
    return await errorResponse(error);
  }
};

const deleteReportRequest = async (request, response) => {
  try {
    await deleteReportRequestService(request.params.report_request_id);
    return response.status(202).json({
      success: true,
      message: "successful",
      details: null,
      data: null,
    });
  } catch (error) {
    return await errorResponse(error);
  }
};

export {
  createReport,
  getReportByRequestById,
  getAllReportCreationRequests,
  deleteReportRequest,
};
