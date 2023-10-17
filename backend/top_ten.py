import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        SelectedColumn = req["SelectedColumn"]
        CategoryId = req["CategoryId"]
        Region =  req["Region"]
        SortBy = req["SortBy"]
    
        if SelectedColumn.lower() not in ['videoid', 'channelid']:
            raise ValueError(f"Invalid select column: {SelectedColumn}")
    
        if SortBy.lower() not in ['viewcount', 'likes']:
            raise ValueError(f"Invalid sort column: {SortBy}")
    
        result = query(f"select {SelectedColumn} from Video where CategoryId = '{CategoryId}' and Region = '{Region}' and TrendingDate = (select max(TrendingDate) from Video) order by {SortBy} DESC limit 10")

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