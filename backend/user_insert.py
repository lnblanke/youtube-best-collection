import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
        
        Password = req.get("Password")
        UserName = req.get("UserName")
        Gender = req.get("Gender")
        Avatar = req.get("Avatar")

        assert Password is not None, "Password is empty"
        assert UserName is not None and UserName != "", "UserName is empty"

        assert not any(c in UserName for c in "\"'()[]\{\}"), "UserName contains invalid character"
        assert not any(c in Password for c in "\"'()[]\{\}"), "Password contains invalid character"

        username = query(f"select UserName from UserInfo where UserName = '{UserName}'")
        assert len(username) == 0, "User with UserName already exists"

        update_cols = ["Password", "UserName"]
        update_items = [f"'{Password}'", f"'{UserName}'"]

        if Gender:
            update_cols.append("Gender")
            update_items.append(f"'{Gender}'")
        if Avatar:
            update_cols.append("Avatar")
            update_items.append(f"'{Avatar}'")

        query(f"insert into UserInfo({', '.join(update_cols)}) values ({', '.join(update_items)})")

        return {
          "isBase64Encoded" : True,
          "statusCode": 201,
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