import aws_cdk as core
import aws_cdk.assertions as assertions

from network_stack.network_stack import AwsServerlessStudentAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_serverless_student_app/aws_serverless_student_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsServerlessStudentAppStack(app, "aws-serverless-student-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
