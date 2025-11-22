import boto3
import json
from time import time

def lambda_handler(event, context):
    # 1. Obtener tenant_id desde body o query params
    tenant_id = None

    # Body
    raw_body = event.get("body")
    if raw_body:
        try:
            body = json.loads(raw_body)
            tenant_id = body.get("tenant_id")
        except:
            pass

    # Query Params
    if not tenant_id and event.get("queryStringParameters"):
        tenant_id = event["queryStringParameters"].get("tenant_id")

    if not tenant_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "tenant_id is required"})
        }

    now = str(int(time()))
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("dev-t_tenant")

    # 2. Update: marcar como inactivo
    update_expression = "SET isActive = :isActive, updatedAt = :updatedAt"
    expression_attribute_values = {
        ":isActive": False,
        ":updatedAt": now
    }

    table.update_item(
        Key={"tenant_id": tenant_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Tenant deactivated", "tenant_id": tenant_id})
    }
