from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime, timedelta
import os
import pandas as pd
import json
from utils import get_connection, get_request_body, query
import yaml

cnx = get_connection(yaml.safe_load(open("config.yaml"))["database"])
cursor = cnx.cursor()

def update_category(path):
    for _, _, files in os.walk(path):
        for file in files:
            if file[-4:] == "json":
                with open(path + file) as f:
                    file = json.load(f)

                    update_query = ""

                    for category in file["items"]:
                        id, title = int(category["id"]), category["snippet"]["title"]
                        update_query += f"({id}, '{title}'),";
                            
                    if update_query != "":
                        cursor.execute(f"insert ignore into Category(CategoryId, CategoryName) values " + update_query[:-1])

def update_videos(path, time):
    for _, _, files in os.walk(path):
        for file in files:
            if file[-3:] == "csv":
                df = pd.read_csv(path + file)

                df.sort_values("trending_date")
                df["trending_date"] = pd.to_datetime(df["trending_date"]).dt.tz_localize(None)
                df["publishedAt"] = pd.to_datetime(df["publishedAt"]).dt.tz_localize(None)

                # Add new videos
                new_df = df[df["trending_date"] >= time - timedelta(days = 2)].reset_index()
                new_df = new_df.drop_duplicates(subset = ["video_id"], keep = "first", ignore_index = True)

                insert_videos, insert_channel, delete_videos, insert_tags = [], [], [], []

                for _, row in new_df.iterrows():
                    row.title = row.title.replace("\"", "\\\"").replace("\\", "\\\\")
                    row.channelTitle = row.channelTitle.replace("\"", "\\\"").replace("\\", "\\\\")
                    
                    insert_videos.append(f"('{row.video_id}', '{file[:2]}', \"{row.title}\", timestamp('{row.publishedAt}'), {row.likes}, timestamp('{row.trending_date}'), {row.view_count}, '{row.thumbnail_link}', '{row.channelId}', {row.categoryId})")
                    insert_channel.append(f"('{row.channelId}', \"{row.channelTitle}\")")
                    delete_videos.append(f"'{row.video_id}'")

                    for tag in row.tags.split("|"):
                        if tag == "" or tag == "[None]":
                            continue
                        tag = tag.strip().replace("\"", "\\\"").replace("\\", "\\\\")
                        insert_tags.append(f"('{row.video_id}', \"{tag}\")")

                if len(insert_channel) > 0:
                    cursor.execute("insert ignore into Channel(ChannelId, ChannelTitle) values " + ", ".join(insert_channel))
                if len(insert_videos) > 0:
                    cursor.execute("replace into Video(VideoId, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, ChannelId, CategoryId) values " + ", ".join(insert_videos))

                if len(delete_videos) > 0:
                    cursor.execute(f"delete from TagOf where VideoId in ({', '.join(delete_videos)})")

                if len(insert_tags) > 0:
                    cursor.execute("insert ignore into TagOf(VideoId, Tag) values " + ", ".join(insert_tags))

                # Compute last week data
                now = datetime.now()
                cur_week_start = now - timedelta(days = (now.weekday() + 1) % 7,
                                                          hours = now.hour,
                                                          minutes = now.minute,
                                                          seconds = now.second)
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
                        viewcount_change = (row.view_count - last_trending.at[0, "view_count"]) / ((row.trending_date - last_trending.at[0, "trending_date"]).days + 1)
                        likes_change = (row.likes - last_trending.at[0, "likes"]) / ((row.trending_date - last_trending.at[0, "trending_date"]).days + 1)
                        
                    cursor.execute(f"update Video set ViewCountChange = {viewcount_change}, LikesChange = {likes_change}, TrendingCount = {trending_count} where VideoId = '{row.video_id}' and Region = '{file[:2]}'")

def update_db(path):
    time = query("select max(UpdateTime) from Config where UpdateItem = 'Video' and Status <> 'F'")[0][0]

    if time is None:
        time = datetime.strptime("2023-09-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    if datetime.now() - time < timedelta(days = 1):
        return
    
    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query(f"insert into Config(UpdateItem, UpdateTime, Status) values ('Video', timestamp('{cur_time}'), 'I')")

    try: 
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(dataset = "rsrishav/youtube-trending-video-dataset", path = path, unzip = True)

        update_category(path)
        update_videos(path, time)

        for _, _, files in os.walk(path):
            for file in files:
                os.remove(path + file)
        os.rmdir(path)
    except Exception as e:
        query(f"update Config set Status = 'F' where UpdateItem = 'Video' and UpdateTime = timestamp('{cur_time}')")
        raise e

    query(f"update Config set Status = 'S' where UpdateItem = 'Video' and UpdateTime = timestamp('{cur_time}')")

def update_weekly_best():
    pass

def lambda_handler(event, context):
    error = None
    path = yaml.safe_load(open("/opt/config.yaml"))["data"]["path"]

    try:
        cnx.start_transaction()
        update_db(path)
        update_weekly_best()
        cnx.commit()
        cursor.close()
    except Exception as e:
        error = e
        
    return get_request_body("PUT", None, error) 

# print(lambda_handler(None, None))