import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";
import { config } from "./config.js";

// Initialize DynamoDB client
let dynamodbClient;

// Create DynamoDB client instance based on config.DYNAMODB_ENDPOINT value
if (config.DYNAMODB_ENDPOINT && config.DYNAMODB_ENDPOINT !== "") {
  dynamodbClient = new DynamoDBClient({
    region: config.AWS_REGION,
    endpoint: config.DYNAMODB_ENDPOINT,
  });
} else {
  dynamodbClient = new DynamoDBClient({ region: config.AWS_REGION });
}
// Create a DocumentClient
const documentClient = DynamoDBDocumentClient.from(dynamodbClient, {
  marshallOptions: { removeUndefinedValues: true },
});
// Export documentClient
export { documentClient };
