from aws_cdk import Stack, CfnOutput
from aws_cdk import aws_dynamodb as ddb
from constructs import Construct

class DatabaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table for context
        self.context_table = ddb.Table(
            self, "DBContextTable",
            table_name="DropBoxContext",
            partition_key=ddb.Attribute(
                name="user_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST  # Use on-demand billing mode
        )

        # DynamoDB table for appointments
        self.appointment_table = ddb.Table(
            self, "DBAppointmentTable",
            table_name="DropBoxAppointment",
            partition_key=ddb.Attribute(
                name="appointment_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST  # Use on-demand billing mode
        )

        # Outputs for the table names
        CfnOutput(self, "ContextTableName", value=self.context_table.table_name)
        CfnOutput(self, "AppointmentTableName", value=self.appointment_table.table_name)
