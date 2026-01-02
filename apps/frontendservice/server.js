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
app.use(express.static(path.resolve(config.REPORT_OUTPUT_FOLDER)));
// Morgan logging middleware
app.use(morgan("combined"));
// Application Routes
app.use(ReportCreationRoute);
app.use(ReportsDefinitionRouter);
// Only start the server when not running tests. Jest sets NODE_ENV=test.
if (process.env.NODE_ENV != "test") {
  app.listen(config.PORT, () =>
    console.log(
      `🌐 The server is running in ${config.NODE_ENV} mode on port ${config.PORT}`
    )
  );
}

export default app;
