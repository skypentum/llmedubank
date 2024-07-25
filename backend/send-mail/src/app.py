import boto3
from botocore.exceptions import ClientError
import os
import configparser

ENV_TYPE = os.getenv('envType', 'LOCAL')
config_file = "config.ini"

config = configparser.ConfigParser()
config.read(config_file)


session = boto3.Session(
    aws_access_key_id=config.get(ENV_TYPE, 'AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config.get(ENV_TYPE, 'AWS_SECRET_ACCESS_KEY'),
    region_name= config.get(ENV_TYPE, 'REGION_NAME')
)


def lambda_handler(event, context):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = config.get(ENV_TYPE, 'SENDER')

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = config.get(ENV_TYPE, 'RECIPIENT')

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-west-2"

    # The subject line for the email.
    SUBJECT = "AI문제은행이 당신에게 문제를 보냅니다."

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (f"AI문제은행이 당신에게 문제를 보냅니다.\r\n아래 URL을 클릭하여 문제를 풀이하세요. {config.get(ENV_TYPE, 'EMAIL_URL')}?dfnId={event['dfnId']}&userId={event['userId']}&stdCnt={event['stdCnt']}"
                )
                
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>AI문제은행이 당신에게 문제를 보냅니다.</p>
    <p>아래 URL을 클릭하여 문제를 풀이하세요. </p>
    <p>{config.get(ENV_TYPE, 'EMAIL_URL')}/preview.html?dfnId={event['dfnId']}&userId={event['userId']}&stdCnt={event['stdCnt']}</p>
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = session.client('ses')

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )

        return {
            "status": 200,
            "message": f"success {response['MessageId']}"
        }
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            "status": 500,
            "message": e.response['Error']['Message']
        }