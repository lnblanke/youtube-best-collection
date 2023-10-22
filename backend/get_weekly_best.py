import json
from utils import query, get_request_body
import datetime

def lambda_handler(event, context):
    result, error = None, None
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
        
        result = query(f"select * from WeeklyBest natural join Video where Week = timestamp('{Week}')")
    except Exception as e:
        error = e

    return get_request_body("GET", result, error)