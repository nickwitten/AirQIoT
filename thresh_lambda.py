import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time


AWS_ACCESS_KEY="AKIAQ42M53PMNY553ZUM"
AWS_SECRET_ACCESS_KEY="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"
AWS_REGION="us-east-1"

def send_email(email_addr, subject, body):
    """ Send an email to specified address containing data """
    # Create a new SES resource and specify a region.
    ses = boto3.client('ses',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': [email_addr],
            },
            Message={
                'Body': {
                    'Text': {
                        'Data': body
                    },
                },
                'Subject': {
                    'Data': subject
                },
            },
            Source='nwitt12@gmail.com'
        )
        # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        
def check_thresh():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=AWS_REGION)

    table = dynamodb.Table('AirQualityDataOutput')
    now=int(time.time())
    timestampold=now-86400
    results = table.scan(
        FilterExpression=Attr('timestamp').gt(timestampold) & Attr('aqi').gt(0)
    )
    return len(results['Items']) > 0
    

if __name__ == '__main__':
    while True:
        if check_thresh():
            message = "Warning, the air quality is bad right now."
            send_email('nwitt12@gmail.com', 'Air Quality Update', message)
        time.sleep(20)

