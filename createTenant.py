import boto3, json, uuid
from time import time
from decimal import Decimal

# Conversor recursivo: float → Decimal
def convert_to_decimal(obj):
    if isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    elif isinstance(obj, float) or isinstance(obj, int):
        return Decimal(str(obj))
    return obj

# Conversor recursivo: Decimal → float (para respuestas JSON)
def decimal_to_float(obj):
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    # Parse body string → dict
    body = event.get("body", "{}")
    if isinstance(body, str):
        body = json.loads(body)

    # Convert all numbers → Decimal for DynamoDB
    body = convert_to_decimal(body)

    # Generate tenant ID
    tenant_id = str(uuid.uuid4())
    now = str(int(time()))

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("dev-t_tenant")

    tenant_data = {
        "tenant_id": tenant_id,
        "name": body["name"],
        "location": {
            "address": body["location"]["address"],
            "city": body["location"]["city"],
            "lat": body["location"]["lat"],
            "lng": body["location"]["lng"]
        },
        "phone_number": body.get("phone_number"),
        "manager": {
            "name": body["manager"]["name"],
            "email": body["manager"]["email"].lower(),
            "staff_id": body["manager"]["staff_id"].lower()
        },
        "opening_hours": body.get("opening_hours", []),
        "delivery_zones": body.get("delivery_zones", []),
        "isActive": True,
        "createdAt": now,
        "updatedAt": now
    }

    # Save to DynamoDB
    table.put_item(Item=tenant_data)

    # Convert Decimal → float for JSON response
    response_tenant = decimal_to_float(tenant_data)

    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Tenant created",
            "tenant_id": tenant_id,
            "tenant": response_tenant
        })
    }
