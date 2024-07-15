import json
import boto3
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE'))

def handler(event, context):
    try:
        if event['httpMethod'] == 'POST' and event['path'] == '/subscribe':
            return subscribe(event)
        elif event['httpMethod'] == 'GET' and event['path'] == '/unsubscribe':
            return unsubscribe(event)
        elif event['httpMethod'] == 'GET' and event['path'] == '/send-email':
            return send_email()
        else:
            return {'statusCode': 404, 'body': json.dumps('Not Found')}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}

def subscribe(event):
    body = json.loads(event['body'])
    email = body['email']
    table.put_item(Item={'email': email, 'subscribed': True})
    return {'statusCode': 200, 'body': json.dumps('Subscribed')}

def unsubscribe(event):
    email = event['queryStringParameters']['email']
    table.update_item(
        Key={'email': email},
        UpdateExpression='SET subscribed = :val',
        ExpressionAttributeValues={':val': False}
    )
    return {'statusCode': 200, 'body': json.dumps('Unsubscribed')}

def send_email():
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('subscribed').eq(True))
    emails = [item['email'] for item in response['Items']]
    
    # Simulate sending email
    send_to_all(emails, "Subject: Newsletter", "This is the content of the email.")
    
    return {'statusCode': 200, 'body': json.dumps(f'Email sent to {len(emails)} subscribers')}

def send_to_all(emails, subject, body):
    # Dummy function to simulate sending email
    for email in emails:
        print(f'Sending email to: {email}')
    print('Emails sent successfully')