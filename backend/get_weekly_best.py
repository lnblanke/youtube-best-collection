import json
from utils import query, get_request_body
import datetime

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        req = event["queryStringParameters"]
        
        Week = req.get("Week")

        assert Week is not None, "Week is empty"

        Week = datetime.datetime.strptime(Week, "%Y-%m-%d")
        Week = Week - datetime.timedelta(days = (Week.weekday() + 1) % 7,
                                         hours = Week.hour,
                                         minutes = Week.minute,
                                         seconds = Week.second)
        
        w = query(f"select Week from WeeklyBest where Week = timestamp('{Week}')")
        assert len(w) > 0, "Week does not exist"
        
        result = query(f"select VideoId, Week, Title, max(ViewCount), max(Likes) from WeeklyBest natural join Video where Week = timestamp('{Week}') group by VideoId, Title, Week")
        
        outputs = []
        
        for [VideoId, Week, Title, ViewCount, Likes] in result:
            outputs.append({
                "VideoId": VideoId,
                "Week": Week,
                "Title": Title,
                "ViewCount": ViewCount,
                "Likes": Likes
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)