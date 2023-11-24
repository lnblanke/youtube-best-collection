import json
from utils import query, get_request_body
import datetime

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        req = event["queryStringParameters"]
        
        Week = req.get("Week")

        assert Week is not None, "Week is empty"

        Week = datetime.datetime.strptime(Week, "%Y-%m-%d %H:%M:%S")
        Week = Week - datetime.timedelta(days = (Week.weekday() + 1) % 7,
                                         hours = Week.hour,
                                         minutes = Week.minute,
                                         seconds = Week.second)
        
        w = query(f"select Week from WeeklyBest where Week = timestamp('{Week}')")
        assert len(w) > 0, "Week does not exist"
        
        result = query(f"select * from WeeklyBest natural join Video natural join Channel natural join Category where Week = timestamp('{Week}')")
        
        outputs = []
        
        for [CategoryId, ChannelId, VideoId, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, LikesChange, ViewCountChange, _, _, _, ChannelTitle, CategoryTitle] in result:
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