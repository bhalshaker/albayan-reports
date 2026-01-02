import {
  createReportDefinitionService,
  getReportDefinitionByTemplateIdService,
  updateReportDefinitionService,
  deleteReportDefinitionService,
  listAllReportDefinitionsService,
} from "../services/database.js";
import errorResponse from "../utils/errorResponse.utils.js";

// Get All Report Definitions Controller
const getAllReportDefinitions = async (request, response) => {
  try {
    // Fetch all report definitions from the database
    const allReportsDefinitions = await listAllReportDefinitionsService();
    // Send successful response with the fetched data
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: allReportsDefinitions,
    });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

// Create Report Definition Controller
const createReportDefinition = async (request, response) => {
  try {
    // Ensure a file was uploaded
    if (!request.file) {
      throw new Error("Please upload a template file");
    }
    // Prepare payload with request body and uploaded file info
    const payload = {
      ...request.body,
      template_file: request.file.filename,
    };
    // Create a new report definition in the database
    const createdReportDefinition = await createReportDefinitionService(
      payload
    );
    // Send successful response with the created report definition
    return response.status(201).json({
      success: true,
      message: "successful",
      details: null,
      data: createdReportDefinition,
    });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

// Get Report Definition By ID Controller
const getReportDefinitionById = async (request, response) => {
  try {
    // Fetch the report definition by template ID from the database
    const reportDefinition = await getReportDefinitionByTemplateIdService(
      request.params.reportDefinitionId
    );
    // Send appropriate response based on whether the definition was found
    if (reportDefinition)
      return response.status(200).json({
        success: true,
        message: "successful",
        details: null,
        data: reportDefinition,
      });
    else
      return response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

const updateReportDefinitionById = async (request, response) => {
  try {
    // Check if the report definition exists
    const reportDefinition = await getReportDefinitionByTemplateIdService(
      request.params.reportDefinitionId
    );
    // If not found, return 404 response
    if (!reportDefinition)
      return response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
    // Ensure a file was uploaded
    if (!request.file) {
      throw new Error("Please upload a template file");
    }
    // Prepare payload with request body and uploaded file info (if any)
    const payload = {
      ...request.body,
      template_file: request.file?.filename,
    };
    // Update the report definition in the database
    const updatedReportDefinition = await updateReportDefinitionService(
      request.params.reportDefinitionId,
      payload
    );
    // Send successful response with the updated report definition
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: updatedReportDefinition,
    });
  } catch (error) {
    // Handle any errors using the errorResponse utility
    return errorResponse(error, response);
  }
};

// Delete Report Definition Controller
const deleteReportDefinition = async (request, response) => {
  try {
    // Check if the report definition exists
    const reportDefinition = await getReportDefinitionByTemplateIdService(
      request.params.reportDefinitionId
    );
    // If not found, return 404 response
    if (!reportDefinition)
      return response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
    // Delete the report definition from the database
    await deleteReportDefinitionService(request.params.reportDefinitionId);
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
  getAllReportDefinitions,
  createReportDefinition,
  getReportDefinitionById,
  updateReportDefinitionById,
  deleteReportDefinition,
};
