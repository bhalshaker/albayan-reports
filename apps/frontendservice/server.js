import express from "express";
import path from "path";
import morgan from "morgan";
import { config } from "./albayanfrontapi/configs/config.js";
import { ReportCreationRoute } from "./albayanfrontapi/routes/ReportCreation.route.js";
import { ReportsDefinitionRouter } from "./albayanfrontapi/routes/ReportDefinition.route.js";

// Initilize Express application
const app = express();
// Enable JSON parsing for incoming requests
app.use(express.json());
// Serve files from that folder
app.use("/output", express.static(path.resolve(config.REPORT_OUTPUT_FOLDER)));
// Morgan logging middleware
app.use(morgan("combined"));
// Application Routes
app.use(ReportCreationRoute);
app.use(ReportsDefinitionRouter);
// Only start the server when not running tests. Jest sets NODE_ENV=test.
if (process.env.NODE_ENV != "test") {
  app.listen(config.PORT, () => {
    console.log(
      `🌐 The server is running in ${config.NODE_ENV} mode on port ${config.PORT}`
    );
    console.log(
      `📁 Generated reports folder location is ${config.REPORT_OUTPUT_FOLDER}`
    );
    console.log(`📁 Reports templates location is ${config.UPLOAD_FOLDER}`);
    console.log(
      `🛢️  Dynamodb definition table is ${config.DEFINITION_TABLE} and processing table is ${config.PROCESSING_TABLE}`
    );
    console.log(`📑 Dynamodb URL ${config.DYNAMODB_ENDPOINT}`);
    console.log(
      `☁️  AWS Region ${config.AWS_REGION},🪪  AWS Access Key ${config.AWS_ACCESS_KEY_ID},🔑 AWS Key ${config.AWS_SECRET_ACCESS_KEY} `
    );
  });
}

export default app;
