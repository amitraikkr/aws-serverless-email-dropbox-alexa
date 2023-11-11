# compute_stack.py
from aws_cdk import Stack, aws_lambda, aws_lambda_destinations, aws_s3, aws_ses_actions, aws_ses, aws_iam, aws_secretsmanager, aws_lambda_event_sources, CfnOutput
from aws_cdk.aws_s3_notifications import LambdaDestination

from constructs import Construct

from database_stack.database_stack import DatabaseStack

class ComputeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, database_stack: DatabaseStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # S3 bucket for storing emails
        email_bucket = aws_s3.Bucket(self, "DropBoxEmailBucket")


        # IAM role for Lambda functions
        lambda_role = aws_iam.Role(
            self, "dropBoxLambdaExecutionRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ]
        )

        # Secret Manager for OpenAI API key
        secret = aws_secretsmanager.Secret(self, "OpenAIApiKey")

        lambda_layer = aws_lambda.LayerVersion(self, "MyLayer",
            code=aws_lambda.Code.from_asset("lib/python"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11],
            description="A layer for shared libraries")



        # Lambda function for processing emails
        lambda_Email_function = aws_lambda.Function(
            self, "EmailProcessingLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="lambda_handler.handler",
            code=aws_lambda.Code.from_asset("lambda_email"),
            environment={
                "TABLE_NAME": database_stack.context_table.table_name,
                "SECRET_ARN": secret.secret_arn
            },
            role=lambda_role,
            layers=[lambda_layer]
        )

        # Grant Lambda function access to the context DynamoDB table
        database_stack.context_table.grant_full_access(lambda_Email_function)

        # Grant Lambda function access to the secret
        secret.grant_read(lambda_Email_function)
        

        lambda_appoint_function = aws_lambda.Function(
            self, "AlexaResponseLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="lambda_handler.handler",
            code=aws_lambda.Code.from_asset("lambda_appoint"),
            environment={
                "TABLE_NAME": database_stack.appointment_table.table_name
            },
            role=lambda_role,
            layers=[lambda_layer]
        )

        # Grant Lambda function access to the appointment DynamoDB table
        database_stack.appointment_table.grant_full_access(lambda_appoint_function)
        

         # S3 event trigger for Lambda function
        s3_event = aws_lambda_event_sources.S3EventSource(
            bucket=email_bucket,
            events=[aws_s3.EventType.OBJECT_CREATED],
            filters=[aws_s3.NotificationKeyFilter(prefix="emails/")]
        )
        
        
        lambda_Email_function.add_event_source(s3_event)

        

        ses_receipt_rule_set = aws_ses.ReceiptRuleSet(self, "MySESReceiptRuleSet",
            # You can add additional configuration here if needed
        )

        # Add the action to a receipt rule
        ses_receipt_rule_set.add_rule("MyRule",
            recipients=["example@example.com"],
            actions=[
                aws_ses_actions.S3(
                    bucket=email_bucket,
                    object_key_prefix="emails/"
                )
            ]
        )


        # Outputs
        CfnOutput(self, "EmailBucketName", value=email_bucket.bucket_name)
        CfnOutput(self, "Lambda1FunctionName", value=lambda_Email_function.function_name)
        CfnOutput(self, "Lambda2FunctionName", value=lambda_appoint_function.function_name)
        CfnOutput(self, "SecretArn", value=secret.secret_arn)