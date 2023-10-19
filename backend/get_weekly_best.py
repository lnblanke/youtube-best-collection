import json
from sql_query import query
import datetime

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        
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

        return {
          "isBase64Encoded" : True,
          "statusCode": 200,
          "headers": {},
          "body": json.dumps({
              "data": result
          }, default = str)
        }
    except Exception as e:
        return {
          "isBase64Encoded" : True,
          "statusCode": 400,
          "headers": {},
          "body": json.dumps({
              "error_message": str(e)
          })
        }