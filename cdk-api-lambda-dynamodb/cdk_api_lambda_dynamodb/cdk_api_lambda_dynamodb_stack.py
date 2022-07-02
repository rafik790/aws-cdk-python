from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
     aws_iam as iam,
     aws_s3 as s3,
     aws_dynamodb as dynamodb
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkApiLambdaDynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        requestTable  = dynamodb.Table(
            self,"request-table",
            table_name="request",
            partition_key={
                "name":"id",
                "type":dynamodb.AttributeType.STRING
            },
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        integrationResponse: _apigw.IntegrationResponse = _apigw.IntegrationResponse(status_code="200")
        methodResponse: _apigw.MethodResponse = _apigw.MethodResponse(status_code="200")
        stage = _apigw.StageOptions(stage_name='dev')

        api = _apigw.RestApi(
            self, "cdk-api-practice",
            rest_api_name='cdk-api-practice',
            deploy=True,
            deploy_options=stage
        )
        api.root.add_method("ANY")

        lambdaResource = api.root.add_resource("save-data-dynmodb")
        requestHandler = _lambda.Function(
            self, 'save-request-dynamodb',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='save_request_data.handler',
            function_name='save-request-dynamodb',
            environment={
                'REQUEST_TABLE':requestTable.table_name
            },
            description="Request handler to insert a request into DynamoDB. Triggered by API Gateway."
        )

        lambdaIntegration = _apigw.LambdaIntegration(
            requestHandler,
            proxy=False,
            integration_responses=[integrationResponse]
        )

        putMethod  = lambdaResource.add_method(
            "PUT",
            integration=lambdaIntegration,
            method_responses=[methodResponse],
            api_key_required=False
        )

        statement = iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[requestTable.table_arn],
            effect=iam.Effect.ALLOW
        )
        requestHandler.add_to_role_policy(statement)




