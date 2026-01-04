# Project Setup Guide

## Prerequisites

Before starting, ensure the following tools are installed on your system:

- **Podman**: A container engine used to run and manage containers.  
  Installation guide: [Podman Official Documentation](https://podman.io/getting-started/installation)

- **Podman Compose**: A tool to run `docker-compose` style workflows with Podman.  
  Typically installed via:

  ```sh
  pip install podman-compose
  ```

- **Terraform**: An infrastructure-as-code tool used to provision resources.  
  Installation guide: [Terraform Official Downloads](https://developer.hashicorp.com/terraform/downloads)

---

## Setup Instructions

### 1. Clone the repository

```sh
git clone https://github.com/bhalshaker/albayan-reports.git
```

### 2. Navigate to the project directory

```sh
cd albayan-reports
```

### 3. Build the environment using Podman Compose

```sh
cd infra/containers
podman-compose up -d --build
```

### 4. Initialize Terraform and create the tables

Navigate to the Terraform directory:

```sh
cd ../terraform
terraform init
```

Apply the Terraform configuration with the required environment variables:

```sh
TF_VAR_is_local=true \
TF_VAR_aws_region=us-east-1 \
TF_VAR_access_key=dummy \
TF_VAR_secret_key=dummy \
TF_VAR_dynamodb=http://localhost:8000 \
terraform apply
```
