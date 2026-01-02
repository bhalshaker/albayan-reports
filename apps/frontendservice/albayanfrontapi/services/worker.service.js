import { config } from "../configs/config.js";
import axios from "axios";

async function createReportFromWorker(report_request_id) {
  try {
    const createReportResponse = await axios.get(
      `${config.WORKER_URL}/reports/issue/${report_request_id}`
    );
    return createReportResponse.data;
  } catch (error) {
    console.error(error);
  }
}

export { createReportFromWorker };
