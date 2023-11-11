from aws_cdk import App 
# Ensure you import the NetworkStack and ComputeStack correctly
from compute_stack.compute_stack import ComputeStack
from database_stack.database_stack import DatabaseStack

app = App()

# Instantiate the NetworkStack
database_stack = DatabaseStack(app, "DatabaseStack")
# Now instantiate the ComputeStack, passing in the network_stack
compute_stack = ComputeStack(app, "ComputeStack", database_stack=database_stack)

app.synth()