import json, boto3
def lambda_handler(event, context):
    body = event["body"]
    tenant_id = body["tenant_id"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("t_tenant")
    response = table.get_item(Key={"tenant_id": tenant_id})
    tenant = response["Item"]

    return {
        "statusCode": 200,
        "body": json.dumps({"tenant": tenant})
    }