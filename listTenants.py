import json, boto3
def lambda_handler(event, context):
    table = boto3.resource("dynamodb").Table("t_tenant")

    res = table.scan()

    return {
        "statusCode": 200,
        "body": json.dumps({"tenants": res["Items"]})
    }