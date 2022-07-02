import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_glu_integration.cdk_glu_integration_stack import CdkGluIntegrationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_glu_integration/cdk_glu_integration_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkGluIntegrationStack(app, "cdk-glu-integration")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
