import json
from sql_query import query
import datetime

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        
        CategoryId = req.get("CategoryId")
        Region =  req.get("Region")
        ChannelId = req.get("ChannelId")
        SortBy = req.get("SortBy")
    
        cur = (datetime.datetime.now() - datetime.timedelta(days = 7)).strftime('%Y/%m/%d %H:%M:%S')
    
        sql = f"SELECT * from Video where TrendingDate >= timestamp(\"{cur}\")" 
    
        if CategoryId:
            sql += f" and CategoryId = {CategoryId}"
        if Region:
            sql += f" and Region = '{Region}'"
        if ChannelId:
            sql += f" and ChannelId = {ChannelId}"
        
        if SortBy.lower() not in ['viewcount', 'likes']:
            raise ValueError(f"Invalid sort column: {SortBy}")
        
        sql += f" ORDER BY {SortBy} DESC" 
    
        result =  query(sql)

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