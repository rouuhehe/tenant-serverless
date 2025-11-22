import json
import boto3
from decimal import Decimal

# Convertir Decimal → float para JSON
def decimal_to_float(obj):
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    print("DEBUG EVENT:", json.dumps(event))

    # 1. Obtener tenant_id desde la URL (pathParameters)
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenant_id")

    if not tenant_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing tenant_id in path"})
        }

    # 2. DynamoDB
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("dev-t_tenant")  # <-- ESTA ES TU TABLA REAL

    response = table.get_item(Key={"tenant_id": tenant_id})

    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Tenant not found"})
        }

    tenant = decimal_to_float(response["Item"])

    return {
        "statusCode": 200,
        "body": json.dumps({"tenant": tenant})
    }
