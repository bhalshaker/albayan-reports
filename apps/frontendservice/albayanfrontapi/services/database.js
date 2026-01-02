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

async function createReportDefinitionService(item) {
  item.report_template_id = crypto.randomUUID();
  item.creation_date = new Date().toISOString();
  item.updated_date = new Date().toISOString();
  await documentClient.send(
    new PutCommand({
      TableName: config.DEFINITION_TABLE,
      Item: item,
      ConditionExpression: "attribute_not_exists(report_template_id)",
    })
  );
  return item;
}

async function getReportDefinitionByTemplateIdService(report_template_id) {
  const response = await documentClient.send(
    new GetCommand({
      TableName: config.DEFINITION_TABLE,
      Key: { report_template_id },
    })
  );
  return response.Item || null;
}

async function updateReportDefinitionService(report_template_id, updates) {
  const updateExpression = [];
  const expressionAttributesNames = {};
  const expressionAttributesValues = {
    ":updated_date": new Date().toISOString(),
  };
  for (const [key, value] of Object.entries(updates)) {
    updateExpression.push(`#${key}=:${key}`);
    expressionAttributesNames[`#${key}`] = key;
    expressionAttributesValues[`:${key}`] = value;
  }
  const UpdateExpression = `SET ${updateExpression.join(
    ","
  )},updated_date=:updated_date`;

  const response = await documentClient.send(
    new UpdateCommand({
      TableName: config.DEFINITION_TABLE,
      Key: { report_template_id },
      UpdateExpression,
      ExpressionAttributeNames: expressionAttributesNames,
      expressionAttributesValues: expressionAttributesValues,
      ConditionExpression: "attribute_exists(report_template_id)",
      ReturnValues: "ALL_NEW",
    })
  );
  return response.Attributes;
}

async function deleteReportDefinitionService(report_template_id) {
  await documentClient.send(
    new DeleteCommand({
      TableName: config.DEFINITION_TABLE,
      Key: { report_template_id },
      ConditionExpression: "attribute_exists(report_template_id)",
    })
  );
  return true;
}

async function listAllReportDefinitionsService() {
  const response = await documentClient.send(
    new ScanCommand({ TableName: config.DEFINITION_TABLE })
  );
  return response.Items;
}

async function createReportService(
  report_template_id,
  output_format,
  report_data
) {
  let reportRequest = {
    report_request_id: crypto.randomUUID(),
    report_template_id: report_template_id,
    report_output_format: output_format,
    report_data: report_data,
    request_date: new Date().toISOString(),
    update_date: new Date().toISOString(),
    processing_status: "pending",
  };
  await documentClient.send(
    new PutCommand({
      TableName: config.PROCESSING_TABLE,
      Item: reportRequest,
      ConditionExpression: "attribute_not_exists(report_request_id)",
    })
  );
  return reportRequest;
}

async function deleteReportRequestService(report_request_id) {
  await documentClient.send(
    new DeleteCommand({
      TableName: config.PROCESSING_TABLE,
      Key: { report_request_id },
      ConditionExpression: "attribute_exists(report_request_id)",
    })
  );
  return true;
}
async function getReportRequestByReportRequestIdService(report_request_id) {
  const response = await documentClient.send(
    new GetCommand({
      TableName: config.PROCESSING_TABLE,
      Key: { report_request_id },
    })
  );
  return response.Item || null;
}
async function listReportRequestsService() {
  const response = await documentClient.send(
    new ScanCommand({ TableName: config.PROCESSING_TABLE })
  );
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
