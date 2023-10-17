import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        
        VideoId, UserId = req["VideoId"], req["UserId"]
        query(f"delete from Favorite where VideoId = '{VideoId}' and UserId = {UserId}")
        
        return {
          "isBase64Encoded" : True,
          "statusCode": 200,
          "headers": {},
          "body": json.dumps({
              "message": "success"
          }, default = str)
        }
    except Exception as e:
        return {
          "isBase64Encoded" : True,
          "statusCode": 400,
          "headers": {},
          "body": json.dumps({
              "error_message": str(e)
          })
        }