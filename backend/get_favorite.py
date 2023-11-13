import json
from utils import query, get_request_body

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        req = event["queryStringParameters"]
        
        UserId = req.get("UserId")

        assert UserId is not None and UserId != "", "UserId is empty"
        
        user = query(f"select UserId from UserInfo where UserId = {UserId}")
        assert len(user) > 0, "User with UserId is not found"
        
        result = query(f"select * from Favorite natural join Video where UserId={UserId}")
        
        outputs = []
        
        for [VideoId, UserId, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, LikesChange, ViewCountChange, ChannelId, CategoryId] in result:
            outputs.append({
                "VideoId": VideoId,
                "UserId": UserId, 
                "Region": Region,
                "Title": Title,
                "PublishedAt": PublishedAt,
                "Likes": Likes,
                "TrendingDate": TrendingDate,
                "ViewCount": ViewCount,
                "ThumbnailLink": ThumbnailLink,
                "LikesChange": LikesChange,
                "ViewCountChange": ViewCountChange,
                "ChannelId": ChannelId, 
                "CategoryId": CategoryId
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)