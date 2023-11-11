<h1>A Serverless Application: Email Dropbox for Appointments</h1>
This serverless application utilizes GPT-4's Natural Language Processing capabilities to extract appointment details from emails. The appointment information is then stored in a database, which can be accessed by a custom Alexa skill for user convenience
    <h3>Application Flow</h3>
    <ul>
        <li><strong>Email Reception:</strong>
            <ul>
                <li>Users send an email to a designated Dropbox email ID.</li>
                <li>The email ID is validated and configured in Amazon Simple Email Service (SES).</li>
            </ul>
        </li>
        <li><strong>Email Storage:</strong>
            <ul>
                <li>SES stores received emails in an Amazon Simple Storage Service (S3) bucket.</li>
            </ul>
        </li>
        <li><strong>Email Processing:</strong>
            <ul>
                <li>An AWS Lambda function is triggered by S3's 'put object' event.</li>
                <li>The Lambda function extracts the email content.</li>
            </ul>
        </li>
        <li><strong>Interaction with OpenAI GPT-4:</strong>
            <ul>
                <li>The Lambda function interacts with the OpenAI GPT-4 model.</li>
                <li>GPT-4 analyzes the email for appointment details, as per instruction provided in system prompt</li>
            </ul>
        </li>
        <li><strong>Results Handling:</strong>
            <ul>
                <li>Extracted appointment details are saved in a DynamoDB 'appointment' table.</li>
                <li>All interactions with GPT-4 are logged in a 'context' table.</li>
                <li>If no appointment details are found, an error message is generated.</li>
            </ul>
        </li>
        <li><strong>Error Notification:</strong>
            <ul>
                <li>In case of an error, an Amazon Simple Notification Service (SNS) email is sent to the user.</li>
            </ul>
        </li>
        <li><strong>Alexa Skill Integration:</strong>
            <ul>
                <li>A custom Alexa skill can be developed.</li>
                <li>The skill allows users to ask Alexa about their appointments, pulling data from the DynamoDB appointment table.</li>
            </ul>
        </li>
    </ul>
    <h2>Prerequisites</h2>
    <ul>
        <li>AWS account with access to Lambda, S3, SES, DynamoDB, and SNS.</li>
        <li>AWS CLI installed and configured.</li>
        <li>AWS CDK installed.</li>
        <li>Node.js and npm (for AWS CDK and Alexa skill development).</li>
        <li>Python 3.x for Lambda functions.</li>
        <li>OpenAI API key (for GPT-4 interaction).</li>
    </ul>
<h2>Installation</h2>

1. Clone the Repository:<br>
<b>git clone https://github.com/amitraikkr/aws-serverless-email-dropbox-alexa.git</b><br>
<b>cd your-repository</b>

2. Deploy the All Stacks:<br>
<b>cdk deploy --all</b>

3. Configure SES:
Verify your Dropbox email address in SES.
Set up a receipt rule to store incoming emails to the designated S3 bucket.

4. Set up OpenAI API Key:
Store your OpenAI API key in AWS Secrets Manager and ensure your Lambda function has access to it.

5. Develop the Alexa Custom Skill:
Follow Amazon's documentation to create a custom Alexa skill that queries the DynamoDB appointment table.

<h2>Usage</h2>

<h3>Sending an Email:</h3>
Send an email with appointment details to the configured Dropbox email ID.

<h3>Checking Appointments:</h3>
Ask your Alexa-enabled device about your appointments, which will be fetched from the DynamoDB appointment table via the custom Alexa skill.

<h3>Error Handling:</h3>
In case of no appointment details in an email, an SNS notification will be sent to inform you.

<h2>Limitations</h2>
<ul>
    <li>The system currently only supports plain text emails for appointment extraction.</li>
    <li>Appointment formats in emails need to be consistent for accurate extraction by GPT-4.</li>
    <li>The custom Alexa skill for querying appointments needs to be developed and linked to the user's Alexa account.</li>
    <li>SES email receiving capabilities are subject to AWS's limitations and quotas.</li>
</ul>


<h3>Useful commands</h3>

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


