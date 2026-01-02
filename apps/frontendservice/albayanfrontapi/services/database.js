import { documentClient } from "../configs/dynamo.js";
import { config } from "../configs/config.js";
import {
  PutCommand,
  GetCommand,
  UpdateCommand,
  DeleteCommand,
  ScanCommand,
} from "@aws-sdk/lib-dynamodb";
import crypto from "crypto";

// Report Definition Services
async function createReportDefinitionService(item) {
  // Generate unique ID and timestamps
  item.report_template_id = crypto.randomUUID();
  item.creation_date = new Date().toISOString();
  item.updated_date = new Date().toISOString();
  // Insert into DynamoDB
  await documentClient.send(
    new PutCommand({
      TableName: config.DEFINITION_TABLE,
      Item: item,
      ConditionExpression: "attribute_not_exists(report_template_id)",
    })
  );
  // Return the created item
  return item;
}

// Fetch Report Definition by ID
async function getReportDefinitionByTemplateIdService(report_template_id) {
  // Fetch item from DynamoDB
  const response = await documentClient.send(
    new GetCommand({
      TableName: config.DEFINITION_TABLE,
      Key: { report_template_id },
    })
  );
  // Return the item or null if not found
  return response.Item || null;
}

// Update Report Definition
async function updateReportDefinitionService(report_template_id, updates) {
  // Initialize update expression components
  const updateExpression = [];
  // Initialize attribute name and value maps
  const expressionAttributesNames = {};
  // Build update expressions
  const expressionAttributesValues = {
    ":updated_date": new Date().toISOString(),
  };
  // Loop through updates to construct the expression
  for (const [key, value] of Object.entries(updates)) {
    updateExpression.push(`#${key}=:${key}`);
    expressionAttributesNames[`#${key}`] = key;
    expressionAttributesValues[`:${key}`] = value;
  }
  // Finalize the UpdateExpression
  const UpdateExpression = `SET ${
    updateExpression.length ? updateExpression.join(",") + "," : ""
  }updated_date=:updated_date`;
  // Execute the update command
  const response = await documentClient.send(
    new UpdateCommand({
      TableName: config.DEFINITION_TABLE,
      Key: { report_template_id },
      UpdateExpression,
      ExpressionAttributeNames: expressionAttributesNames,
      ExpressionAttributeValues: expressionAttributesValues,
      ConditionExpression: "attribute_exists(report_template_id)",
      ReturnValues: "ALL_NEW",
    })
  );
  // Return the updated attributes
  return response.Attributes;
}

// Delete Report Definition
async function deleteReportDefinitionService(report_template_id) {
  // Execute the delete command
  await documentClient.send(
    new DeleteCommand({
      TableName: config.DEFINITION_TABLE,
      Key: { report_template_id },
      ConditionExpression: "attribute_exists(report_template_id)",
    })
  );
  // Return true on successful deletion
  return true;
}

// List All Report Definitions
async function listAllReportDefinitionsService() {
  // Scan the table to get all report definitions
  const response = await documentClient.send(
    new ScanCommand({ TableName: config.DEFINITION_TABLE })
  );
  // Return the list of items
  return response.Items;
}

// Report Creation Services
async function createReportService(
  report_template_id,
  output_format,
  report_data
) {
  // Create a new report request item
  let reportRequest = {
    report_request_id: crypto.randomUUID(),
    report_template_id: report_template_id,
    report_output_format: output_format,
    report_data: report_data,
    request_date: new Date().toISOString(),
    update_date: new Date().toISOString(),
    processing_status: "pending",
  };
  // Insert the report request into DynamoDB
  await documentClient.send(
    new PutCommand({
      TableName: config.PROCESSING_TABLE,
      Item: reportRequest,
      ConditionExpression: "attribute_not_exists(report_request_id)",
    })
  );
  // Return the created report request
  return reportRequest;
}

// Delete Report Request
async function deleteReportRequestService(report_request_id) {
  // Execute the delete command
  await documentClient.send(
    new DeleteCommand({
      TableName: config.PROCESSING_TABLE,
      Key: { report_request_id },
      ConditionExpression: "attribute_exists(report_request_id)",
    })
  );
  // Return true on successful deletion
  return true;
}

// Get Report Request by ID
async function getReportRequestByReportRequestIdService(report_request_id) {
  // Fetch the report request from DynamoDB
  const response = await documentClient.send(
    new GetCommand({
      TableName: config.PROCESSING_TABLE,
      Key: { report_request_id },
    })
  );
  // Return the item or null if not found
  return response.Item || null;
}

// List All Report Requests
async function listReportRequestsService() {
  // Scan the table to get all report requests
  const response = await documentClient.send(
    new ScanCommand({ TableName: config.PROCESSING_TABLE })
  );
  // Return the list of items
  return response.Items;
}

export {
  createReportDefinitionService,
  getReportDefinitionByTemplateIdService,
  updateReportDefinitionService,
  deleteReportDefinitionService,
  listAllReportDefinitionsService,
  createReportService,
  deleteReportRequestService,
  getReportRequestByReportRequestIdService,
  listReportRequestsService,
};
