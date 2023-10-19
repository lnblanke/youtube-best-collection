import kaggle
from datetime import datetime, timedelta
import os
import pandas as pd
import json
from sql_query import query
from time import time
import yaml

def update_category():
    for _, _, files in os.walk("./data/"):
        for file in files:
            if file[-4:] == "json":
                with open("./data/" + file) as f:
                    file = json.load(f)

                    update_query = ""

                    for category in file["items"]:
                        id, title = int(category["id"]), category["snippet"]["title"]
                        update_query += f"({id}, '{title}'),";
                            
                    if update_query != "":
                        query(f"insert ignore into Category(CategoryId, CategoryName) values " + update_query[:-1])

def update_videos(time):
    for _, _, files in os.walk("./data/"):
        for file in files:
            if file[-3:] == "csv":
                df = pd.read_csv("./data/" + file)

                df.sort_values("trending_date")
                df["trending_date"] = pd.to_datetime(df["trending_date"]).dt.tz_localize(None)

                df = df[df["trending_date"] >= time - timedelta(days = 2)].reset_index()

                new_rows = df.drop_duplicates(subset = ["video_id"], keep = "first", ignore_index = True)
                new_rows.insert(len(df.columns), "like_change", new_rows["likes"])
                new_rows.insert(len(df.columns) + 1, "view_count_change", new_rows["view_count"])

                df = pd.merge(df, new_rows, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
                df = df.drop_duplicates(subset = ["video_id"], keep = "first", ignore_index = True)

                insert_videos, insert_channel, delete_videos, insert_tags = "", "", "", ""

                for idx, row in new_rows.iterrows():
                    old_row = df.loc[df["video_id"] == row.video_id]

                    if len(old_row) != 0:
                        new_rows.at[idx, "view_count_change"] = row.view_count - old_row["view_count"]
                        new_rows.at[idx, "like_change"] = row.likes - old_row["likes"]

                    row.title = row.title.replace("\"", "'").replace("\\", "")
                    row.channelTitle = row.channelTitle.replace("\"", "'").replace("\\", "")

                    insert_videos += f"('{row.video_id}', '{file[:2]}', \"{row.title}\", timestamp('{row.publishedAt}'), {row.likes}, timestamp('{row.trending_date}'), {row.view_count}, '{row.thumbnail_link}', {row.like_change}, {row.view_count_change}, '{row.channelId}', {row.categoryId}),"
                    insert_channel += f"('{row.channelId}', \"{row.channelTitle}\"),"
                    delete_videos += f"'{row.video_id}',"

                    for tag in row.tags.split("|"):
                        if tag == "" or tag == "[None]":
                            continue
                        tag = tag.strip().replace("\"", "'").replace("\\", "")
                        insert_tags += f"('{row.video_id}', \"{tag}\"),"

                if insert_channel != "":
                    query("insert ignore into Channel(ChannelId, ChannelTitle) values " + insert_channel[:-1])

                if insert_videos != "":
                    query("replace into Video(VideoId, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, LikesChange, ViewCountChange, ChannelId, CategoryId) values " + insert_videos[:-1])

                if delete_videos != "":
                    query(f"delete from TagOf where VideoId in ({delete_videos[:-1]})")

                if insert_tags != "":
                    query("insert ignore into TagOf(VideoId, Tag) values " + insert_tags[:-1])

def update():
    time = query("select max(UpdateTime) from Config where UpdateItem = 'Video' and Status <> 'F'")[0][0]

    if time is None:
        time = datetime.strptime("2023-09-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    if datetime.now() - time < timedelta(days = 1):
        return
    
    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query(f"insert into Config(UpdateItem, UpdateTime, Status) values ('Video', timestamp('{cur_time}'), 'I')")

    try:    
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('rsrishav/youtube-trending-video-dataset', 
                                          path = './data/', unzip = True)
        
        update_category()
        update_videos(time)

        for _, _, files in os.walk("./data/"):
            for file in files:
                os.remove("./data/" + file)
        os.rmdir("./data/")
    except Exception as e:
        query(f"update Config set Status = 'F' where UpdateItem = 'Video' and UpdateTime = timestamp('{cur_time}')")
        raise e

    query(f"update Config set Status = 'S' where UpdateItem = 'Video' and UpdateTime = timestamp('{cur_time}')")

if __name__ == "__main__":
    ts = time()
    update()

    print((time() - ts)/60)