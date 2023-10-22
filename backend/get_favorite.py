import json
from utils import query, get_request_body

def lambda_handler(event, context):
    result, error = None, None
    try:
        req = event["queryStringParameters"]
        
        UserId = req.get("UserId")

        assert UserId is not None and UserId != "", "UserId is empty"
        
        user = query(f"select UserId from UserInfo where UserId = {UserId}")
        assert len(user) > 0, "User with UserId is not found"
        
        result = query(f"select * from Favorite natural join Video where UserId={UserId}")
    except Exception as e:
        error = e

    return get_request_body("GET", result, error)