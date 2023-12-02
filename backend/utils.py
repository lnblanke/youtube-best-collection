import mysql.connector
import yaml
import json

def get_connection(database_config):
    cnx = mysql.connector.connect(
        host = database_config["host"],
        user = database_config["user"],
        password = database_config["password"],
        database = database_config["database"],
        port = database_config["port"]
    )
    return cnx

def query(query):
    cnx = get_connection(yaml.safe_load(open("config.yaml"))["database"])
    cursor = cnx.cursor()

    select = (query[:6].lower() == "select")

    if select:
        cursor.execute("start transaction read only")
    else:
        cursor.execute("start transaction write read")

    cursor.execute(query)

    if select:
        result = cursor.fetchall()
    cnx.commit()
    cursor.close()

    return result if select else None

def get_request_body(method: str, data, error):
    if error is None:
        return {
            "isBase64Encoded": True,
            "statusCode": (201 if method == "POST" else 200),
            "headers": {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': "OPTIONS," + method
            },
            "body": (json.dumps({"data": data}, default=str) if data is not None else json.dumps({"message": "success"}))
        }
    else:
        return {
            "isBase64Encoded": True,
            "statusCode": 400,
            "headers": {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': "OPTIONS," + method
            },
            "body": json.dumps({
                "error_message": str(error)
            })
        }
    
def check_invalid_character(text: str, strict = False):
    if strict:
        return all(c in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+[]|<>,./?" for c in text)
    else:
        return not any(c in text for c in "\"'{}\\")