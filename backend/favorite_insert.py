import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        
        VideoId, UserId = req["VideoId"], req["UserId"]
        
        query(f"insert into Favorite(VideoId, UserId) values ('{VideoId}', '{UserId}')")

        return {
          "isBase64Encoded" : True,
          "statusCode": 201,
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