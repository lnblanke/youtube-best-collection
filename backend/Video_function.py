from sql_query import query
import datetime

def Video_query_by(event, context):
    Region, by_what = event["Region"], event["SortBy"]
    return query(f"select * from Video where Region = '{Region}' order by {by_what} DESC limit 50")

# print(Video_query_by({'Region': 'JP', 'SortBy': 'Likes'}, None))

def top_ten_videos(event):
    selected_column = event["selected_column"]
    CategoryId = event["CategoryId"]
    Region =  event["Region"]
    order_by_column = event["order_by_column"]

    column_can_select = ['VideoId', 'ChannelId']
    column_can_sort = ['ViewCount', 'Likes']

    if selected_column not in column_can_select:
        raise ValueError(f"Invalid select column: {selected_column}")

    if order_by_column not in column_can_sort:
        raise ValueError(f"Invalid sort column: {order_by_column}")

    sql = (f"select {selected_column} from Video where CategoryId = '{CategoryId}' and Region = '{Region}' and TrendingDate = (select max(TrendingDate) from Video) order by {order_by_column} DESC limit 10")
    return query(sql)

# print(top_ten_videos({'selected_column': 'VideoId', 'CategoryId': 17, 'Region': 'FR', 'order_by_column': 'Likes'}))

# print(query(f"select VideoId from Video where CategoryId = 17 and Region = 'FR' and TrendingDate = (select max(TrendingDate) from Video) order by Likes DESC limit 10"))

def sort_trending_videos(event, context):
    CategoryId = event.get("CategoryId")
    Region =  event.get("Region")
    ChannelId = event.get("ChannelId")
    order_by_column = event.get("order_by_column")

    cur = (datetime.datetime.now() - datetime.timedelta(days = 7)).strftime('%Y/%m/%d %H:%M:%S')

    sql = f"SELECT * from Video where TrendingDate >= timestamp(\"{cur}\")" 

    if CategoryId:
        sql += f" and CategoryId = {CategoryId}"
    if Region:
        sql += f" and Region = '{Region}'"
    if ChannelId:
        sql += f" and ChannelId = {ChannelId}"
    
    column_can_sort = ['ViewCount', 'Likes']
    
    if order_by_column not in column_can_sort:
        raise ValueError(f"Invalid sort column: {order_by_column}")
    
    sql += f" ORDER BY {order_by_column} DESC" 

    print(sql)

    return query(sql)

print(sort_trending_videos({'CategoryId': 15, "Region": 'JP', 'order_by_column': 'ViewCount'}, None))



