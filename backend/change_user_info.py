import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        
        UserId = req.get("UserId")
        Password = req.get("Password")
        UserName = req.get("UserName")
        Gender = req.get("Gender")
        Avatar = req.get("Avatar")

        assert UserId is not None, "UserId is empty"
        
        user = query(f"select UserId from UserInfo where UserId='{UserId}'")
        
        assert len(user) > 0, "User with UserId is not found"

        assert not any(c in UserName for c in "\"'()[]\{\}"), "UserName contains invalid character"
        assert not any(c in Password for c in "\"'()[]\{\}"), "Password contains invalid character"

        username = query(f"select UserName from UserInfo where UserName = '{UserName}'")
        assert len(username) == 0, "User with UserName already exists"

        update_cols = []

        if Password:
            update_cols.append(f"Password = '{Password}'")
        if UserName:
            update_cols.append(f"UserName = '{UserName}'")
        if Gender:
            update_cols.append(f"Gender = '{Gender}'")
        if Avatar:
            update_cols.append(f"Avatar = '{Avatar}'")

        query(f"update UserInfo set {', '.join(update_cols)} where UserId = {UserId}")
 
        return {
          "isBase64Encoded" : True,
          "statusCode": 200,
          "headers": {},
          "body": json.dumps({
              "message": "success"
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