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
