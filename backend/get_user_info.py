import json
from utils import query, get_request_body, check_invalid_character

def lambda_handler(event, context):
    result, error = None, None
    try:
        req = event["queryStringParameters"]
        
        UserName = req.get("UserName")

        assert UserName is not None, "UserName is empty"
        assert check_invalid_character(UserName), "UserName contains invalid character"
        
        user = query(f"select UserName from UserInfo where UserName = \"{UserName}\"")
        assert len(user) > 0, "User with UserName is not found"
        
        result = query(f"select * from UserInfo where UserName = \"{UserName}\"")
    except Exception as e:
        error = e

    return get_request_body("GET", result, error)