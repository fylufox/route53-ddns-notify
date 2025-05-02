
def lambda_handler(event, context):
    """
    AWS Lambda function handler.
    """
    # Your code here
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }