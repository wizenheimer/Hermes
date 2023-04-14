import os
import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):    
    
    emailData = event['Records'][0]["messageAttributes"]
    
    SENDER = os.environ["emailSender"]

    RECIPIENT = emailData['toEmail']
    
    print (emailData)
    
    if 'toCCEmail' in emailData:
      CC_RECIPIENT = emailData['toCCEmail']
      DESTINATION={
                        'ToAddresses': [
                            RECIPIENT,
                        ],
                        'CcAddresses': [
                            CC_RECIPIENT,
                        ]
                    }
      
    else:
      DESTINATION = {
                        'ToAddresses': [
                            RECIPIENT,
                        ]
                    }
    
    
    AWS_REGION = "us-east-1"
    
    SUBJECT = emailData['subject']
    
    BODY_HTML = emailData['body']        
    
    CHARSET = "UTF-8"
    
    client = boto3.client('ses',region_name=AWS_REGION)
    
    try:
        
        response = client.send_email(
            Destination = DESTINATION,
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
        
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])
        print(RECIPIENT)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
