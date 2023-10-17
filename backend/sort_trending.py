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
        PageNum = req.get("PageNum")
        VideoPerPage = req.get("VideoPerPage")
    
        cur = (datetime.datetime.now() - datetime.timedelta(days = 7)).strftime('%Y/%m/%d %H:%M:%S')
    
        sql = f"SELECT * from Video where TrendingDate >= timestamp(\"{cur}\")" 
        
        assert SortBy.lower() in ['viewcount', 'likes'], f"Invalid sort column: {SortBy}"
    
        if CategoryId:
            sql += f" and CategoryId = {CategoryId}"
            
            category = query(f"select CategoryId from Category where CategoryId = {CategoryId}")
            assert len(category) > 0, "Category with CategoryId does not exist"
        if Region:
            sql += f" and Region = '{Region}'"
            
            region = query(f"select Region from Video where Region = '{Region}'")
            assert len(region) > 0, "Region does not exist"
        if ChannelId:
            sql += f" and ChannelId = '{ChannelId}'"
            
            channel = query(f"select ChannelId from Channel where ChannelId = '{ChannelId}'")
            assert len(channel) > 0, "Channel with ChannelId does not exist"
        if VideoPerPage is None:
            VideoPerPage = 20
        if PageNum is None:
            PageNum = 0
        
        sql += f" ORDER BY {SortBy} DESC limit {VideoPerPage} offset {PageNum * VideoPerPage}" 
    
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