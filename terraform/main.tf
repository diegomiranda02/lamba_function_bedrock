terraform {
  backend "s3" {
    bucket         = "glpi-bedrock-project-terraform-state"   # Your S3 bucket name
    key            = "path/to/terraform.tfstate"              # Path within the bucket to store the state file
    region         = "us-east-1"                              # AWS region of the S3 bucket
  }
}

# Create IAM role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  })
}

# Attach policies for invoking Bedrock service
resource "aws_iam_role_policy" "lambda_bedrock_policy" {
  name   = "lambda_bedrock_policy"
  role   = aws_iam_role.lambda_exec_role.id
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "bedrock:InvokeModel"
        ],
        "Resource": "*"
      }
    ]
  })
}

# Zip the lambda function code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "lambda_function" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "lambda_function_bedrock"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = filebase64sha256(data.archive_file.lambda_zip.output_path)

  environment {
    variables = {
      BEDROCK_MODEL_ID = "meta.llama3-70b-instruct-v1:0"
    }
  }
}

# Create API Gateway
resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "llm_test"
  protocol_type = "HTTP"
}

# Create API Gateway route
resource "aws_apigatewayv2_route" "api_route" {
  api_id    = aws_apigatewayv2_api.api_gateway.id
  route_key = "POST /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Integrate Lambda with API Gateway
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.api_gateway.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.lambda_function.invoke_arn
}

# Deploy API
resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "dev"
  auto_deploy = true
}

# Grant API Gateway permission to invoke Lambda
resource "aws_lambda_permission" "apigw_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api_gateway.execution_arn}/*/*"
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.api_gateway.api_endpoint
}
