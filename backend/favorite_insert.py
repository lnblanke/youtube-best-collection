import json
from utils import query, get_request_body

def lambda_handler(event, context):
    error = None
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
        assert len(favorite) == 0, "Favorite with VideoId and UserId already exists"
        
        query(f"insert into Favorite(VideoId, UserId) values ('{VideoId}', '{UserId}')")
    except Exception as e:
        error = e

    return get_request_body("POST", None, error)