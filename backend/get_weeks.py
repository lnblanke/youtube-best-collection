import json
from utils import query, get_request_body
from datetime import datetime

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        result = query(f"select * from Week order by Week desc")
        
        outputs = [] 
        
        for [week] in result:
            outputs.append({
                "value": datetime.strftime(week, "%Y-%m-%d"),
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)