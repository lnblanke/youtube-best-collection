import mysql.connector
import yaml

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
    cnx = get_connection(yaml.safe_load(open("/opt/config.yaml"))["database"])
    cursor = cnx.cursor()
    cnx.start_transaction
    cursor.execute(query)

    select = (query[:6].lower() == "select")

    if select:
        result = cursor.fetchall()
    cnx.commit()
    cursor.close()

    return result if select else None