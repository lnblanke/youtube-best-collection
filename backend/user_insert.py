import json
from utils import query, get_request_body, check_invalid_character

def lambda_handler(event, context):
    error = None
    try:
        req = json.loads(event["body"])
        
        Password = req.get("Password")
        UserName = req.get("UserName")
        Gender = req.get("Gender")
        Avatar = req.get("Avatar")

        assert Password is not None, "Password is empty"
        assert UserName is not None and UserName != "", "UserName is empty"

        assert check_invalid_character(UserName), "UserName contains invalid character"
        assert check_invalid_character(Password, True), "Password contains invalid character"

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
    except Exception as e:
        error = e

    return get_request_body("POST", None, error)