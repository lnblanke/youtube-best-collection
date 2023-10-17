import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        
        VideoId, UserId = req.get("VideoId"), req.get("UserId")

        assert VideoId is not None, "VideoId is empty"
        assert UserId is not None, "UserId is empty"
        
        user = query(f"select UserId from UserInfo where UserId = {UserId}")
        assert len(user) > 0, "User with UserId is not found"
        
        video = query(f"select VideoId from Video where VideoId = '{VideoId}'")
        assert len(video) > 0, "Video with VideoId is not found"
        
        favorite = query(f"select VideoId from Favorite where VideoId = '{VideoId}' and UserId = {UserId}")
        assert len(favorite) > 0, "Favorite with VideoId and UserId is not found"

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