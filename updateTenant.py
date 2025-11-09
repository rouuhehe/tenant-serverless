import boto3, json
from time import time

def lambda_handler(event, context):
    body = json.loads(event['body'])
    tenant_id = body['tenant_id']
    update_fields = body['update_fields']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_tenant')

    update_expression = "SET " + ", ".join(f"{key} = :{key}" for key in update_fields.keys())
    expression_attribute_values = {f":{key}": value for key, value in update_fields.items()}

    response = table.update_item(
        Key={'tenant_id': tenant_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"updated_tenant": response["Attributes"]})
    }