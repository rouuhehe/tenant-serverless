import boto3, json, uuid
from time import time

def lambda_handler(event, context):
    body = event["body"]

    tenant_id = body["tenant_id"]
    item_id = str(uuid.uuid4())
    now = str(int(time()))

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("t_tenant")

    tenant_data = {
        "tenant_id": tenant_id,
        "name": body["name"],
        "location": {
            "address": body["location"]["address"],
            "city": body["location"]["city"],
            "lat": body["location"]["lat"],
            "lng": body["location"]["lng"],
        },
        "phone_number": body.get("phone_number"),
        "manager": {
            "name": body["manager"]["name"],
            "email": body["manager"]["email"].lower(),
        "staff_id": body["manager"]["staff_id"].lower(),
        },
        "opening_hours": body.get("opening_hours", []),
        "delivery_zones": body.get("delivery_zones", []),
        "isActive": True,
        "createdAt": now,
        "updatedAt": now
    }

    table.put_item(Item=tenant_data)
    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Tenant created",
            "tenant_id": tenant_id,
            "tenant": tenant_data
        })
    }
