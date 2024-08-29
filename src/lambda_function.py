import json
import boto3

bedrock_runtime = boto3.client("bedrock-runtime", "us-east-1")

def model_invocation(model_id: str, params: dict) -> str:
    # The body is now directly the params dictionary
    body = params
    
    print("Model ID:", model_id)
    print("Request Body:", json.dumps(body, indent=2))

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json"
        )
        
        response_content = response['body'].read()
        response_data = json.loads(response_content)
        
        # Access the generated text correctly from the response structure
        result = response_data.get('generation', '')
        print("Result:" + str(result))
        
        return result
        
    except Exception as e:
        exception_message = f"Error generating the response: {e}"
        print(exception_message)
        return exception_message

def lambda_handler(event, context):
    try:
        # Check if 'body' exists in the event
        if 'body' in event:
            event_body = json.loads(event['body'])  # Parsing the body JSON string to a dictionary
            model_id = event_body.get('model_id', "mistral.mistral-7b-instruct-v0:2")  # Default model ID if not provided
            params = event_body.get('params', {})  # Expecting params to already be a dictionary

        else:
            print("Event does not contain 'body'. Full event:", event)
            return {
                'statusCode': 400,
                'body': json.dumps({'error': "Request body is missing or invalid!"})
            }

        if 'prompt' not in params:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': "Prompt is missing"})
            }

        # Call model_invocation with model_id and the params dictionary
        response = model_invocation(model_id, params)

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': "Invalid JSON in request body"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
