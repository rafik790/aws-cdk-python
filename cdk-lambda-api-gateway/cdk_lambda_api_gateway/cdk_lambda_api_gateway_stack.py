from unicodedata import name
from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
     aws_iam as iam,
     aws_s3 as s3,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkLambdaApiGatewayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        """cdk_lambda_hello = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
            function_name='CDKLambdaFun'
        )
        apiHello = _apigw.LambdaRestApi(
            self,
            id="api-of-test-api-lambda",
            handler=cdk_lambda_hello,
            deploy=True,
            deploy_options=_apigw.StageOptions(stage_name='dev'),
            rest_api_name='cdk-gateway-api',
            proxy=False
        )
        apiHello.root.add_method("GET")
        """

        
        integrationResponse: _apigw.IntegrationResponse = _apigw.IntegrationResponse(status_code="200")
        methodResponse: _apigw.MethodResponse = _apigw.MethodResponse(status_code="200")
        stage = _apigw.StageOptions(stage_name='dev')
        
        api = _apigw.RestApi(
            self, "cdk-gw-api",
            rest_api_name='cdk-gw-api',
            deploy=True,
            deploy_options=stage
        )
        api.root.add_method("ANY")
        
        lambdaResource = api.root.add_resource("lambda")
        cdk_lambda_api_key_test = _lambda.Function(
            self, 'CDKAPIKeyHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='api_key_test.handler',
            function_name='CDKAPIKeyLambdaFun'
        )


        lambdaIntegration = _apigw.LambdaIntegration(
            cdk_lambda_api_key_test,
            proxy=False,
            integration_responses=[integrationResponse]
        )


        getMethod  = lambdaResource.add_method(
            "GET",
            integration=lambdaIntegration,
            method_responses=[methodResponse],
            api_key_required=True
        )

        throttlingForGetMethod = _apigw.ThrottlingPerMethod(
            method=getMethod,
            throttle=_apigw.ThrottleSettings(rate_limit=100,burst_limit=5)
        )

        test_usage_plan = api.add_usage_plan(
            id="ckd-test-api-key-plan",
            name='cdk-test-usage-plan',
            throttle=_apigw.ThrottleSettings(rate_limit=100,burst_limit=5),
            quota=_apigw.QuotaSettings(limit=1000,period=_apigw.Period.WEEK)
        )

        key = api.add_api_key(id='cdk-test-api-key',api_key_name='cdk-test-api-key')
        test_usage_plan.add_api_key(key)

        test_usage_plan.add_api_stage(
            api=api,
            stage=api.deployment_stage,
            throttle=[throttlingForGetMethod]
        )

        #CODE TO LIST OBJECT FROM S3
        rest_api_role: iam.Role = iam.Role(
            self,
            "CDKRestAPIRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")]
        )

        bucket: s3.Bucket = s3.Bucket(
            self, "CDKWidgetStore",
            bucket_name="cdk-gateway-api-raf"
        )

        list_objects_response: _apigw.IntegrationResponse = _apigw.IntegrationResponse(status_code="200")
        list_objects_integration_options: _apigw.IntegrationOptions = _apigw.IntegrationOptions(
            credentials_role=rest_api_role,
            integration_responses=[list_objects_response],
        )

        getBucketObjectsIntegration: _apigw.AwsIntegration = _apigw.AwsIntegration(
            service="s3",
            integration_http_method="GET",
            path=bucket.bucket_name,
            options=list_objects_integration_options
        )

        
        bucketObjectResource = api.root.add_resource("bucket-objects")
        bucketObjectResource.add_method(
            "GET",
            getBucketObjectsIntegration,
            method_responses=[methodResponse],
            api_key_required=True
        )
        #END-CODE TO LIST OBJECT FROM S3
        
