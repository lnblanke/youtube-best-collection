import mysql.connector

def get_connection():
    cnx = mysql.connector.connect(
        host="mysql-database.cvz0vt1mykn7.us-east-2.rds.amazonaws.com",
        user="admin",
        password="edgerunners",
        database="youtube",
        port="3306"
    )
    return cnx

def query(query):
    cnx = get_connection()
    cursor = cnx.cursor()
    cnx.start_transaction
    cursor.execute(query)

    select = (query[:6].lower() == "select")

    if select:
        result = cursor.fetchall()
    cnx.commit()
    cursor.close()

    return result if select else None