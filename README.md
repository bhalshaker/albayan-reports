# 📄 Albayan Reports

![Albayan Reports Logo](docs/images/AlbayanReportsLogo.png)

Albayan Reports is an open-source reporting engine designed for seamless integration into new or existing enterprise application stacks.

It enables organizations to generate static reports from custom OpenOffice/LibreOffice templates. Reports can be delivered in native OpenOffice/LibreOffice formats or print-ready PDFs, with full support for embedding text, dynamic tables, and images. Albayan standardizes reporting across teams while offering complete flexibility in template design.

Built on a scalable, multi-service architecture utilizing **Express**, **FastAPI**, **S3**, **Kafka MQ**, and **DynamoDB**, the system is engineered to support multi-user environments, automated CI/CD pipelines, and containerized deployments.

Future development will focus on evolving Albayan into a vendor-neutral, extensible reporting solution that enterprises can confidently adopt across diverse cloud environments.

---

## 📊 Features at a Glance

| Category              | Highlights                                                                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Report Generation** | Static reports from custom OpenOffice/LibreOffice templates, exported as native formats or PDFs.                                                        |
| **Content Support**   | Text, tables, and dynamic images                                                                                                                        |
| **APIs**              | REST endpoints for report definitions, issuance, retrieval, and deletion                                                                                |
| **Architecture**      | Express + FastAPI + DynamoDB for definitions & metadata; S3 for templates and generated reports; Kafka MQ for communication between Express and FastAPI |
| **Scalability**       | Multi-user support, issuance tracking, MQ integration planned                                                                                           |
| **Security**          | API key authentication for controlled enterprise access                                                                                                 |
| **Deployment**        | Containerized (Podman/Kubernetes), AWS DynamoDB required, cloud-agnostic                                                                                |
| **Automation**        | CI/CD pipelines with Jenkins & GitHub Actions; Terraform & Ansible scripts                                                                              |
| **Testing**           | Automated testing with Jest, SuperTest, and Pytest                                                                                                      |
| **Open Source**       | Documentation, examples, and sample templates included in the GitHub repository                                                                         |
| **Future Vision**     | Vendor-neutral, extensible reporting system for diverse environments                                                                                    |

---

## 📂 Repository Structure

```
/albayan-reports/
├── apps/ # Deployable services
│   ├── api-fastapi/ # Python/FastAPI service (handles report generation)
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── service-express/ # Node/Express service (handles report creation & management)
│       ├── src/
│       ├── Dockerfile
│       ├── package.json
│       └── server.js
│
├── infra/ # Deployment & infrastructure configuration
│   ├── containers/ # Shared Docker setup
│   ├── terraform/ # IaC for cloud setup (e.g., DynamoDB, ECS, load balancers)
│   └── ci-cd/ # Pipeline scripts
│
├── docs/ # Documentation
│   ├── architecture.md # Express ↔ FastAPI flow
│   ├── templates.md # Guide to creating OpenOffice/LibreOffice templates
│   ├── project_setup_and_deployment.md # Production deployment guide
│   ├── application_usage_example.md # API usage examples
│   └── api-spec.yaml # OpenAPI/Swagger spec for Express service
│
├── templates/ # Example templates
│   ├── attendance_report_template.ods
│   ├── invoice_template.odt
│   ├── monthly_dashboard_template.odp
│   └── transaction_statement_template.odt
│
├── .gitignore
└── README.md # Project overview
```

---

## 📡 API Endpoints

### 🛣️ Express Endpoints

| HTTP Method | Endpoint                            | Description                           | Access           |
| ----------- | ----------------------------------- | ------------------------------------- | ---------------- |
| GET         | `/reports`                          | List all report definitions           | API Key required |
| POST        | `/reports`                          | Define a new report                   | API Key required |
| GET         | `/reports/:reportId`                | Retrieve a specific report definition | API Key required |
| PUT         | `/reports/:reportId`                | Update a specific report definition   | API Key required |
| DELETE      | `/reports/:reportId`                | Delete a specific report definition   | API Key required |
| POST        | `/reports/:reportId/issue`          | Issue a new report                    | API Key required |
| GET         | `/reports/:reportId/issue`          | List all issued reports               | API Key required |
| GET         | `/reports/:reportId/issue/:issueId` | Retrieve an issued report             | API Key required |
| DELETE      | `/reports/:reportId/issue/:issueId` | Delete an issued report               | API Key required |

### 🛤️ FastAPI Endpoints

| HTTP Method | Endpoint                  | Description               | Access |
| ----------- | ------------------------- | ------------------------- | ------ |
| POST        | `/reports/issue`          | Request report generation | Public |
| GET         | `/reports/issue/:issueId` | Retrieve generated report | Public |

---

## 🛠️ Technologies Used

### ☕️ ExpressJS

| Tool/Library                 | Purpose                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| **express**                  | Web framework for building server-side applications          |
| **ajv**                      | Schema-based validator for request payloads                  |
| **dotenv**                   | Loads environment variables from `.env` into `process.env`   |
| **@aws-sdk/client-s3**       | AWS SDK for S3 integration                                   |
| **@aws-sdk/client-dynamodb** | AWS SDK for DynamoDB integration                             |
| **@aws-sdk/lib-dynamodb**    | DynamoDB helper utilities                                    |
| **kafkajs**                  | Kafka client for Node.js                                     |
| **cors**                     | Middleware for enabling CORS                                 |
| **jest**                     | JavaScript testing framework                                 |
| **supertest**                | HTTP assertions for testing APIs                             |
| **nodemon**                  | Development utility for auto-restarting Node.js applications |

### 🐍 FastAPI

| Tool/Library  | Purpose                                                   |
| ------------- | --------------------------------------------------------- |
| **fastapi**   | Web framework for building server-side applications       |
| **uvicorn**   | ASGI server for running FastAPI apps                      |
| **websocket** | Real-time communication support                           |
| **pyuno**     | LibreOffice/OpenOffice integration for template rendering |
| **aiokafka**  | Kafka client for Python                                   |
| **boto3**     | AWS SDK for Python                                        |
| **pytest**    | Python testing framework                                  |

### 🦭 Container Images

| Image                     | Purpose                          |
| ------------------------- | -------------------------------- |
| **amazon/dynamodb-local** | Local DynamoDB emulation         |
| **apache/kafka**          | Message queue service            |
| **minio/minio**           | Local S3-compatible object store |

---

## 📘 Application Guides

- [System Architecture](docs/architecture.md)
- [Template Creation Guide](docs/templates.md)
- [Project Setup & Deployment Guide](docs/project_setup_and_deployment.md)
- [Application Usage Examples](docs/application_usage_example.md)
