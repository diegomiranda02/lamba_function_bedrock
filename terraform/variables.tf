variable "lambda_function_name" {
  type        = string
  description = "The name of the Lambda function"
  default     = "lambda_function_bedrock"
}

variable "api_gateway_name" {
  type        = string
  description = "The name of the API Gateway"
  default     = "llm_test"
}

variable "api_stage_name" {
  type        = string
  description = "The name of the API Gateway stage"
  default     = "dev"
}

variable "s3_bucket" {
  type        = string
  description = "The name of the S3 bucket to store the Terraform state"
}

variable "s3_key_path" {
  type        = string
  description = "The path to store the Terraform state in the S3 bucket"
}

variable "aws_region" {
  type        = string
  description = "The AWS region for the resources"
}
