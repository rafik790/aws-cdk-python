from aws_cdk import (
    # Duration,
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_s3 as s3, 
    aws_s3_deployment as s3deploy,
    aws_glue as glue,                                                                                 
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkGluIntegrationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        role = iam.Role(self, "MyRole",assumed_by=iam.ServicePrincipal("glue.amazonaws.com"))

        gluePolicy = iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
        role.add_managed_policy(gluePolicy)

        s3FullAccessPolicy = iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        role.add_managed_policy(s3FullAccessPolicy)

        """statement = iam.PolicyStatement(
            actions=["ecr:*"],
            resources=['*'],
            effect=iam.Effect.ALLOW
        )

        ecrPolicy = iam.Policy(
            self,
            id='ecr-policy',
            statements=[statement],
            policy_name='ckd-glujob-ecr'
        )
        role.attach_inline_policy(ecrPolicy)"""

        """ecrPloicy = iam.ManagedPolicy.from_managed_policy_arn(
            self,
            id="ckd-glujob-ecr",
            managed_policy_arn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
        )
        role.attach_inline_policy(ecrPloicy)"""

        glueScriptBucket = s3.Bucket(
            self, 
            "GlueScriptBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        glueScriptBucket.grant_read_write(role)


        s3deploy.BucketDeployment(
            self, 'DeployGlueJobFiles',
            destination_bucket=glueScriptBucket,
            sources=[s3deploy.Source.asset('./resources/glue-scripts')],
            destination_key_prefix='Scripts'
        )

        processDataJobName = 'fetch-fifa-data'
        GLUE_VERSION = "2.0"
        PYTHON_VERSION = "3"
        COMMAND_NAME = "pythonshell"
        glue.CfnJob(
            self, 
            id=processDataJobName,
            name=processDataJobName,
            role=role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name=COMMAND_NAME,
                python_version=PYTHON_VERSION,
                script_location="s3://" + glueScriptBucket.bucket_name + "/Scripts/get-concatinate-fifa-data.py"
            ),
            default_arguments={'--JOB_NAME':processDataJobName,'--source_bucket': 'glu-fifa-data-2022'},
            glue_version=GLUE_VERSION
        )




        