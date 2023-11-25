import json
from utils import query, get_request_body

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        result = query(f"select * from Week")
        
        outputs = [] 
        
        for [week] in result:
            outputs.append({
                "value": week,
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)