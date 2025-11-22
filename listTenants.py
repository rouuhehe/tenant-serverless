import json
import boto3
from decimal import Decimal

def decimal_to_float(obj):
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    table = boto3.resource("dynamodb").Table("dev-t_tenant")

    res = table.scan()
    tenants = decimal_to_float(res.get("Items", []))

    return {
        "statusCode": 200,
        "body": json.dumps({"tenants": tenants})
    }
