import boto3, json, uuid
from time import time

def lambda_handler(event, context):
    body = event["body"]

    tenant_id = body["tenant_id"]
    now = str(int(time()))

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("t_tenant")

    update_expression = "SET isActive = :isActive, updatedAt = :updatedAt"
    expression_attribute_values = {
        ":isActive": False,
        ":updatedAt": now
    }

    table.update_item(
        Key={
            "tenant_id": tenant_id,
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Tenant deactivated", "tenant_id": tenant_id}),
    }