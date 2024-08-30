variable "project_name" {
  type        = string
  description = "The name of the GitHub project"
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

variable "lambda_timeout" {
  type        = number
  description = "The timeout for the Lambda function in seconds"
  default     = 240  # Default to 4 minutes
}
