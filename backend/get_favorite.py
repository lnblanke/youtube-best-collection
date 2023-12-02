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
        
        result = query(f"select * from (select VideoId, Title from Favorite natural join Video natural join Channel natural join Category where UserId={UserId} order by TrendingDate desc) as t group by VideoId")
        
        outputs = []
        
        for [VideoId, Title] in result:
            outputs.append({
                "VideoId": VideoId,
                "Title": Title
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)