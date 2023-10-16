from sql_query import query

# Favorite
# print(query("insert into Favorite(VideoId, UserId) values (\"___cBGMDQcE\", 2)"))

# print(query("delete from Favorite where UserId = 2"))

def favorite_insert (event, context):
    VideoId, UserId = event["VideoId"], event["UserId"]
    query(f"insert into Favorite(VideoId, UserId) values ('{VideoId}', '{UserId}')")

# favorite_insert ({'VideoId': '___cBGMDQcE', 'UserId': 2}, None)

def favorite_delete (event, context):
    VideoId, UserId = event["VideoId"], event["UserId"]
    query(f"delete from Favorite where VideoId = '{VideoId}' and UserId = {UserId}")

# favorite_delete ({'VideoId': '___cBGMDQcE', 'UserId': 2}, None)

#-----------------------------------------------------------------------------------------
