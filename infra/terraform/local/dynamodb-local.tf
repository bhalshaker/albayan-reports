terraform{
    required_providers {
      aws={
        source = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
}

provider "aws" {
    region = "us-west-2"
    access_key = "dummy"
    secret_key = "dummy"
    skip_credentials_validation = true
    skip_requesting_account_id = true

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

    # Other attributes
    # attribute {
    #   name="template_file"
    #   type = "S"
    # }
    # attribute {
    #   name="template_file_type"
    #   type = "S"
    # }
    # attribute {
    #   name="creation_date"
    #   type = "S"
    # }
    # attribute {
    #   name="updated_date"
    #   type = "S"
    # }
  
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
    # Other attributes
    # attribute {
    #   name="report_template_id"
    #   type = "S"
    # }
    # attribute {
    #   name="report_output_format"
    #   type = "S"
    # }
    # attribute {
    #   name="template_file_type"
    #   type = "S"
    # }
    # attribute {
    #   name="request_date"
    #   type = "S"
    # }
    # attribute {
    #   name="update_date"
    #   type = "S"
    # }
    # attribute {
    #   name="processing_status"
    #   type = "S"
    # }
  
}