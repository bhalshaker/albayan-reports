terraform{
    required_providers {
      aws={
        source = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
}

variable "is_local" {
  type=bool
  default=true
}
variable "aws_region" {}
variable "access_key" {}
variable "secret_key" {}
variable "dynamodb" {}

provider "aws" {
    region                      = var.aws_region
    access_key                  = var.access_key
    secret_key                  = var.secret_key
    skip_credentials_validation = var.is_local
    skip_requesting_account_id  = var.is_local

    # This is the correct way to define service endpoints in AWS Provider v5
    endpoints {
      dynamodb = var.dynamodb
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