from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime, timedelta
import os
import pandas as pd
import json
from utils import get_connection, query
import yaml

cnx = get_connection(yaml.safe_load(open("/opt/config.yaml"))["database"])
cursor = cnx.cursor()

category_id_mapping = {}

def update_category(path):
    categories = {}
    
    for _, _, files in os.walk(path):
        for file in files:
            if file[-4:] == "json":
                with open(path + file) as f:
                    file = json.load(f)

                    for category in file["items"]:
                        id, title = int(category["id"]), category["snippet"]["title"]
                        categories[id] = title  

    update_query = []

    for (i, key) in enumerate(categories.keys()):
        category_id_mapping[key] = i

        update_query.append(f"({i}, \"{categories[key]}\")")

    cursor.execute(f"insert ignore into Category(CategoryId, CategoryName) values {', '.join(update_query)}")

def update_videos(path, time):
    for _, _, files in os.walk(path):
        for file in files:
            if file[-3:] == "csv":
                df = pd.read_csv(path + file)

                df = df.sort_values("trending_date", ascending = False)

                df["trending_date"] = pd.to_datetime(df["trending_date"]).dt.tz_localize(None)
                df["publishedAt"] = pd.to_datetime(df["publishedAt"]).dt.tz_localize(None)

                # Add new videos
                new_df = df[df["trending_date"] >= time - timedelta(days = 2)].reset_index()
                new_df = new_df.drop_duplicates(subset = ["video_id"], keep = "first", ignore_index = True)

                prev_df = pd.merge(df, new_df, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
                prev_df = prev_df.drop_duplicates(subset = ["video_id"], keep = "first", ignore_index = True)

                insert_videos, insert_channel, delete_videos, insert_tags = [], [], [], []

                for _, row in new_df.iterrows():
                    prev_row = prev_df.loc[prev_df["video_id"] == row.video_id]

                    if len(prev_row) == 0:
                        likes_change = row.likes / (max((row.trending_date - row.publishedAt).days, 0) + 1)
                        viewcount_change = row.view_count / (max((row.trending_date - row.publishedAt).days, 0) + 1)
                    else:
                        prev_row = prev_row.iloc[0]
                        likes_change = (row.likes - prev_row.likes) / (row.trending_date - prev_row.trending_date).days
                        viewcount_change = (row.view_count - prev_row.view_count) / (row.trending_date - prev_row.trending_date).days

                    row.channelTitle = row.channelTitle.replace("\\", "\\\\").replace("\"", "\\\"")
                    
                    insert_videos.append(f"('{row.video_id}', '{file[:2]}', \"{row.title}\", timestamp('{row.publishedAt}'), {row.likes}, timestamp('{row.trending_date}'), {row.view_count}, '{row.thumbnail_link}', '{row.channelId}', {category_id_mapping[row.categoryId]}, {likes_change}, {viewcount_change})")
                    insert_channel.append(f"('{row.channelId}', \"{row.channelTitle}\")")
                    delete_videos.append(f"'{row.video_id}'")

                    for tag in row.tags.split("|"):
                        if tag == "" or tag == "[None]":
                            continue
                        tag = tag.strip().replace("\\", "\\\\").replace("\"", "\\\"")
                        insert_tags.append(f"('{row.video_id}', \"{tag}\")")

                if len(insert_channel) > 0:
                    cursor.execute("insert ignore into Channel(ChannelId, ChannelTitle) values " + ", ".join(insert_channel))
                if len(insert_videos) > 0:
                    cursor.execute("replace into Video(VideoId, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, ChannelId, CategoryId, LikesChange, ViewCountChange) values " + ", ".join(insert_videos))

                if len(delete_videos) > 0:
                    cursor.execute(f"delete from TagOf where VideoId in ({', '.join(delete_videos)})")

                if len(insert_tags) > 0:
                    cursor.execute("insert ignore into TagOf(VideoId, Tag) values " + ", ".join(insert_tags))

                # Compute last week data
                cursor.execute("update Video set TrendingCount = 0, WeeklyViewCountChange = 0, WeeklyLikesChange = 0 where TrendingCount > 0")
                
                now = datetime.now()
                cur_week_start = now - timedelta(days = (now.weekday() + 1) % 7,
                                                 hours = now.hour,
                                                 minutes = now.minute,
                                                 seconds = now.second + 1)
                last_week_start = cur_week_start - timedelta(days = 7)

                last_week_df = df[(df["trending_date"] >= last_week_start) & (df["trending_date"] < cur_week_start)].reset_index()
                last_week_unique = last_week_df.drop_duplicates(subset = ["video_id"], keep = "first", ignore_index = True)

                for _, row in last_week_unique.iterrows():
                    trending_count = len(last_week_df[last_week_df["video_id"] == row.video_id])
                    last_trending = df[(df["video_id"] == row.video_id) & (df["trending_date"] < last_week_start)].reset_index()

                    if len(last_trending) == 0:
                        viewcount_change = row.view_count / (max((row.trending_date - row.publishedAt).days, 0) + 1)
                        likes_change = row.likes / (max((row.trending_date - row.publishedAt).days, 0) + 1)
                    else:
                        viewcount_change = (row.view_count - last_trending.at[0, "view_count"]) / (row.trending_date - last_trending.at[0, "trending_date"]).days
                        likes_change = (row.likes - last_trending.at[0, "likes"]) / (row.trending_date - last_trending.at[0, "trending_date"]).days
                        
                    try:
                        cursor.execute(f"update Video set WeeklyViewCountChange = {viewcount_change}, WeeklyLikesChange = {likes_change}, TrendingCount = {trending_count} where VideoId = '{row.video_id}' and Region = '{file[:2]}'")
                    except:
                        pass

def update_db(path):
    time = query("select max(UpdateTime) from Config where Status <> 'F' and UpdateItem = 'Video'")[0][0]

    if time is None:
        time = datetime.strptime("2023-09-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    if datetime.now() - time < timedelta(days = 1):
        return
    
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query(f"insert into Config(UpdateItem, UpdateTime, Status) values ('Video', timestamp('{now_str}'), 'I')")
    
    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(dataset = "rsrishav/youtube-trending-video-dataset", path = path, unzip = True)

        cursor.execute("start transaction read write")

        update_category(path)
        update_videos(path, time)

        for _, _, files in os.walk(path):
            for file in files:
                os.remove(path + file)
        os.rmdir(path)

        cursor.execute("commit")
        query(f"update Config set Status = 'S' where UpdateItem = 'Video' and UpdateTime = timestamp('{now_str}')")
    except Exception as e:
        cursor.execute("rollback")
        e = e.replace("\"", "\\\"").replace("\\", "\\\\")
        query(f"update Config set Status = 'F', Extra = \"{e}\" where UpdateItem = 'Video' and UpdateTime = timestamp('{now_str}')")

def update_weekly_best(Week: datetime):
    max_week = query("select max(Week) from Week")[0][0]

    if max_week is not None and datetime.strftime(max_week, '%Y-%m-%d %H:%M:%S') >= datetime.strftime(Week, '%Y-%m-%d %H:%M:%S'):
        return
    
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query(f"insert into Config(UpdateItem, UpdateTime, Status) values ('WeeklyBest', timestamp('{now_str}'), 'I')")

    try:
        sql_select = f"""SELECT VideoId, sum(TrendingCount * 1000000 * Weight) + 10 * sum(WeeklyLikesChange) / 11 + sum(WeeklyViewCountChange) / 11 as Score
                        FROM Video NATURAL JOIN RegionWeight 
                        WHERE TrendingCount > 0 AND VideoId NOT IN (select VideoId from WeeklyBest)
                        GROUP BY VideoId
                        ORDER BY Score DESC 
                        LIMIT 10"""

        videos = query(sql_select)

        cursor.execute("start transaction read write")

        for video in videos:
            video_id = video[0]
            sql_insert = f"INSERT INTO WeeklyBest (VideoId, Week) VALUES ('{video_id}', timestamp('{datetime.strftime(Week, '%Y-%m-%d %H:%M:%S')}'))"
            cursor.execute(sql_insert)
        
        cursor.execute("commit")
        query(f"update Config set Status = 'S' where UpdateItem = 'WeeklyBest' and UpdateTime = timestamp('{now_str}')")
    except Exception as e:
        cursor.execute("rollback")
        e = e.replace("\"", "\\\"").replace("\\", "\\\\")
        query(f"update Config set Status = 'F', Extra = \"{e}\" where UpdateItem = 'WeeklyBest' and UpdateTime = timestamp('{now_str}')")

def lambda_handler(event, context):
    path = yaml.safe_load(open("/opt/config.yaml"))["data"]["path"]
    
    now = datetime.now()

    update_db(path)
    update_weekly_best(now - timedelta(days = (now.weekday() + 1) % 7 + 7,
                                       hours = now.hour,
                                       minutes = now.minute,
                                       seconds = now.second))

    cursor.close()