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
        
        result = query(f"select * from Favorite natural join Video natural join Channel natural join Category where UserId={UserId}")
        
        outputs = []
        
        for [CategoryId, ChannelId, VideoId, _, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, LikesChange, ViewCountChange, _, _, _, ChannelTitle, CategoryTitle] in result:
            outputs.append({
                "VideoId": VideoId,
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
                "ChannelTitle": ChannelTitle,
                "CategoryId": CategoryId,
                "CategoryTitle": CategoryTitle
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)