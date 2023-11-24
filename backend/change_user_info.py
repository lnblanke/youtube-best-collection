import json
from utils import query, check_invalid_character, get_request_body

def lambda_handler(event, context):
    error = None
    try:
        req = json.loads(event["body"])
        
        UserId = req.get("UserId")
        Password = req.get("Password")
        UserName = req.get("UserName")
        Gender = req.get("Gender")
        Avatar = req.get("Avatar")

        assert UserId is not None, "UserId is empty"
        
        user = query(f"select UserId from UserInfo where UserId={UserId}")
        
        assert len(user) > 0, "User with UserId is not found"

        update_cols = []

        if Password:
            assert Password != "", "Password is emtpy"
            assert check_invalid_character(Password, True), "Password contains invalid character"
            update_cols.append(f"Password = '{Password}'")
        if UserName:
            assert check_invalid_character(UserName), "UserName contains invalid character"
            
            username = query(f"select UserName from UserInfo where UserName = '{UserName}' and UserId <> {UserId}")
            assert len(username) == 0, "User with UserName already exists"
            
            update_cols.append(f"UserName = '{UserName}'")
        if Gender:
            update_cols.append(f"Gender = '{Gender}'")
        if Avatar:
            update_cols.append(f"Avatar = '{Avatar}'")

        if len(update_cols) > 0:
            query(f"update UserInfo set {', '.join(update_cols)} where UserId = {UserId}")
    except Exception as e:
        error = e

    return get_request_body("PUT", None, error)