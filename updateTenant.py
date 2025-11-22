import boto3
import json
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
    # OBTENER tenant_id DESDE QUERY PARAMS
    query_params = event.get("queryStringParameters") or {}
    tenant_id = query_params.get("tenant_id")

    if not tenant_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "tenant_id is required as query param"})
        }

    # PARSEAR BODY
    raw_body = event.get("body")
    try:
        body = json.loads(raw_body) if raw_body else {}
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON body"})
        }

    # LOS CAMPOS A ACTUALIZAR SON EL BODY MISMO
    update_fields = body

    if not update_fields:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Request body cannot be empty"})
        }

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("dev-t_tenant")

    # BUILD UPDATE EXPRESSION
    update_expression = "SET " + ", ".join(f"{key} = :{key}" for key in update_fields.keys())
    expression_attribute_values = {
        f":{key}": value for key, value in update_fields.items()
    }

    response = table.update_item(
        Key={"tenant_id": tenant_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )

    updated_item = decimal_to_float(response["Attributes"])

    return {
        "statusCode": 200,
        "body": json.dumps({"updated_tenant": updated_item})
    }
