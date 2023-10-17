import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        Region, SortBy = req["Region"], req["SortBy"]
        
        if SortBy.lower() not in ['viewcount', 'likes']:
            raise ValueError(f"Invalid sort column: {SortBy}")
        
        result = query(f"select * from Video where Region = '{Region}' order by {SortBy} DESC limit 50")
        
        return {
          "isBase64Encoded" : True,
          "statusCode": 200,
          "headers": {},
          "body": json.dumps({
              "data": result
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