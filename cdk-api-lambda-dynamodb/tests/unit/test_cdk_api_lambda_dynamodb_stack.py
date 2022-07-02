import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_api_lambda_dynamodb.cdk_api_lambda_dynamodb_stack import CdkApiLambdaDynamodbStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_api_lambda_dynamodb/cdk_api_lambda_dynamodb_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkApiLambdaDynamodbStack(app, "cdk-api-lambda-dynamodb")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
