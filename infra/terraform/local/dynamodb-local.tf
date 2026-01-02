terraform{
    required_providers {
      aws={
        source = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
}

provider "aws" {
    region                      = "us-east-1"
    access_key                  = "dummy"
    secret_key                  = "dummy"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true

    # This is the correct way to define service endpoints in AWS Provider v5
    endpoints {
      dynamodb = "http://localhost:8090"
    }
}

resource "aws_dynamodb_table" "reports_definition" {
    name = "reports_definition"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "report_template_id"

    # Primary key
    attribute {
      name="report_template_id"
      type = "S"
    }
  
}

resource "aws_dynamodb_table" "reports_processing" {
    name = "reports_processing"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "report_request_id"

    # Primary key
    attribute {
      name="report_request_id"
      type = "S"
    }
}