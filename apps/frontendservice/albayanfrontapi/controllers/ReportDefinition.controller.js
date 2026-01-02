import {
  createReportDefinitionService,
  getReportDefinitionByTemplateIdService,
  updateReportDefinitionService,
  deleteReportDefinitionService,
  listAllReportDefinitionsService,
} from "../services/database.js";
import errorResponse from "../utils/errorResponse.utils.js";

const getAllReportDefinitions = async (request, response) => {
  try {
    const allReportsDefinitions = await listAllReportDefinitionsService();
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: allReportsDefinitio + ns,
    });
  } catch (error) {
    return await errorResponse(error);
  }
};

const createReportDefinition = async (request, response) => {
  try {
    if (!request.file) {
      throw new Error("File must be in .odt format");
    }
    const payload = {
      ...request.body,
      template_file: request.file.filename,
    };
    const createdReportDefinition = await createReportDefinitionService(
      payload
    );
    return response.status(201).json({
      success: true,
      message: "successful",
      details: null,
      data: createdReportDefinition,
    });
  } catch (error) {
    return await errorResponse(error);
  }
};

const getReportDefinitionById = async (request, response) => {
  try {
    const reportDefinition = await getReportDefinitionByTemplateIdService(
      request.params.reportDefinitionId
    );
    if (reportDefinition)
      return response.status(200).json({
        success: true,
        message: "successful",
        details: null,
        data: reportDefinition,
      });
    else
      response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
  } catch (error) {
    return await errorResponse(error);
  }
};

const updateReportDefinitionById = async (request, response) => {
  try {
    const reportDefinition = await getReportDefinitionByTemplateIdService(
      request.params.reportDefinitionId
    );
    if (!reportDefinition)
      response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
    const payload = {
      ...request.body,
      template_file: request.file.filename,
    };
    const updatedReportDefinition = await updateReportDefinitionService(
      request.params.reportDefinitionId,
      payload
    );
    return response.status(200).json({
      success: true,
      message: "successful",
      details: null,
      data: updatedReportDefinition,
    });
  } catch (erro) {
    return await errorResponse(error);
  }
};

const deleteReportDefinition = async (request, response) => {
  try {
    const reportDefinition = await getReportDefinitionByTemplateIdService(
      request.params.reportDefinitionId
    );
    if (!reportDefinition)
      response.status(404).json({
        success: false,
        message: "record not found",
        details: null,
        data: null,
      });
    await deleteReportDefinitionService(request.params.reportDefinitionId);
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
  getAllReportDefinitions,
  createReportDefinition,
  getReportDefinitionById,
  updateReportDefinitionById,
  deleteReportDefinition,
};
