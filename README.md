# 📄 Albayan Reports

Albayan Reports is an open source reporting engine designed for seamless integration into new or existing enterprise application stacks.

It empowers organizations to generate static reports from custom OpenOffice/LibreOffice templates. Outputs can be delivered in native OpenOffice/LibreOffice formats or ready to print PDFs, with full support for embedding text, dynamic tables, and images. Albayan standardizes reporting across teams while offering complete flexibility in template design.

Built on a scalable, multi-service architecture utilizing Express, FastAPI, and DynamoDB, the system is engineered to support multi-user environments, automated CI/CD pipelines, and containerized deployments.

Future development will focus on evolving Albayan into a vendor neutral, extensible reporting solution that enterprises can confidently adopt across diverse cloud environments.

## 📂 Repository Structure

---

/albayan-reports/
├── apps/ # Contains the separate, deployable services
│ ├── api-fastapi/ # The Python/FastAPI service (Handles actual reports generation)
│ │ ├── src/
│ │ ├── Dockerfile
│ │ └── requirements.txt
│ │
│ └── service-express/ # The Node/Express service (Handles Reports creation and generation)
│ ├── src/
│ ├── Dockerfile
│ ├── package.json
│ └── server.js
│
├── infra/ # Configuration for automated deployments and infrastructure
│ ├── containers/ # Shared Docker setup
│ ├── terraform/ # Infrastructure as Code (IaC) for cloud setup (e.g., DynamoDB,ECS and load balancers)
│ └── ci-cd/ # Pipeline scripts
│
├── docs/ # User and developer documentation
│ ├── architecture.md # Diagram/explanation of Express <-> FastAPI flow
│ ├── templates.md # Guide to creating OpenOffice/LibreOffice templates
│ ├── project_setup_and_deployment.md # Guide on deploying the system in production
│ ├── application_usage_example.md # Guide on how to use the APIs
│ └── api-spec.yaml # OpenAPI/Swagger spec for Express service
│
├── templates/ # Example/default templates for testing and demonstration
│ ├── attendance_report_template.ods
│ ├── invoice_template.odt
│ ├── monthly_dashboard_template.odp
│ └── transaction_statement_template.odt
│
├── .gitignore
└── README.md # The main project overview

---

## 📡 API Endpoints

---

### 🛣️ Express Endpoints

| HTTP Method | Endpoint                            | Description                           | Who Can Access?            |
| ----------- | ----------------------------------- | ------------------------------------- | -------------------------- |
| GET         | `/reports`                          | List all reports definitions          | Users with a valid API Key |
| POST        | `/reports`                          | Define a new report                   | Users with a valid API Key |
| GET         | `/reports/:reportId`                | Retrieve a specific report definition | Users with a valid API Key |
| PUT         | `/reports/:reportId`                | Update a specific report definition   | Users with a valid API Key |
| DELETE      | `/reports/:reportId`                | Delete a specific report definition   | Users with a valid API Key |
| POST        | `/reports/:reportId/issue`          | Issue a new report                    | Users with a valid API Key |
| GET         | `/reports/:reportId/issue`          | Get all issued reports                | Users with a valid API Key |
| GET         | `/reports/:reportId/issue/:issueId` | Retrieve an issued report             | Users with a valid API Key |
| DELETE      | `/reports/:reportId/issue/:issueId` | Delete an issued report               | Users with a valid API Key |

### 🛤️ FastAPI Endpoints

| HTTP Method | Endpoint                  | Description                 | Who Can Access? |
| ----------- | ------------------------- | --------------------------- | --------------- |
| POST        | `/reports/issue`          | Request a report generation | Public          |
| GET         | `/reports/issue/:issueId` | Get the generated report    | Public          |

---

## 🛠️ Technologies Used

### ExpressJS

| **Tool/Library** | **Purpose**                                                       |
| ---------------- | ----------------------------------------------------------------- |
| **express**      | Web framework for building server-side applications               |
| **avj**          | Schema-based validator for request payloads                       |
| **dotenv**       | Loads environment variables from a `.env` file into `process.env` |

### FastAPI

### LibereOffice
