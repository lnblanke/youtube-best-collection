import kaggle
from datetime import datetime, timedelta
import os
import pandas as pd
import json
import mysql.connector
import numpy as np
from time import time

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

    select = (query[:6] == "select")

    if select:
        result = cursor.fetchall()
    cnx.commit()
    cursor.close()

    return result if select else None

def update_video():
    # time = query("select max(UpdateTime) from Config where UpdateItem = 'Video'")[0][0]
    time = None

    # if time is not None and datetime.now() - time < timedelta(days = 1):
    #     return
    
    # query(f"insert into Config(UpdateItem, UpdateTime) values ('Video', timestamp('{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'))")

    # kaggle.api.authenticate()
    # kaggle.api.dataset_download_files('rsrishav/youtube-trending-video-dataset', 
    #                                   path = './data/', unzip=True)

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
                
    for _, _, files in os.walk("./data/"):
        update_videos = {}
        for file in files:
            if file[-3:] == "csv":
                df = pd.read_csv("./data/" + file)

                df.sort_values("trending_date")
                df["like_change"] = df["view_count_change"] = np.zeros(len(df))

                df["trending_date"] = pd.to_datetime(df["trending_date"]).dt.tz_localize(None)

                if time is not None:
                    df = df[df["trending_date"] >= time - timedelta(days = 2)].reset_index()

                existing_ids = {}
                update_list = set()

                for idx, row in df.iterrows():
                    if row["video_id"] in existing_ids:
                        old_id = existing_ids[row["video_id"]]
                        update_list.remove(old_id)

                        df.at[idx, "like_change"] = row["likes"] - df["likes"][old_id]
                        df.at[idx, "view_count_change"] = row["view_count"] - df["view_count"][old_id]
                    else:
                        df.at[idx, "like_change"] = row["likes"]
                        df.at[idx, "view_count_change"] = row["view_count"]

                    update_list.add(idx)
                    # existing_ids[row["video_id"]] = idx
                    # df.at[idx, "title"] = df.at[idx, "title"].replace('\"', '\'')

                # insert_query = ""

                for idx in update_list:
                #     df.at[idx, "channelTitle"] = df.at[idx, "channelTitle"].replace('\"', '\'')
                #     insert_query += f"('{df.iloc[idx].channelId}', \"{df.iloc[idx].channelTitle}\"),"

                    update_videos[df.at[idx, "video_id"]] = df.at[idx, "tags"].split("|")

                # if insert_query != "":
                #     query("insert ignore into Channel(ChannelId, ChannelTitle) values " + insert_query[:-1])

                # insert_query = ""

                # for idx in update_list:
                #     row = df.iloc[idx]
                #     insert_query += f"('{row.video_id}', '{file[:2]}', \"{row.title}\", timestamp('{row.publishedAt}'), {row.likes}, timestamp('{row.trending_date}'), {row.view_count}, '{row.thumbnail_link}', {row.like_change}, {row.view_count_change}, '{row.channelId}', {row.categoryId}),"

                # if insert_query != "":
                #     query("replace into Video(VideoId, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, LikesChange, ViewCountChange, ChannelId, CategoryId) values " + insert_query[:-1])

        # delete_query, insert_query = "", ""

        for video in update_videos:
            # delete_query += f"'video',"

            insert_query = ""

            for tag in update_videos[video]:
                if tag != "[None]" and tag != "":
                    tag = tag.replace("\"", "'")
                    insert_query += f"('{video}', \"{tag.strip()}\"), "

            if insert_query != "":
                query(f"insert ignore into TagOf(VideoId, Tag) values " + insert_query[:-2])

        # if delete_query != "":
        #     query(f"delete from TagOf where VideoId in ({delete_query[:-1]})")
        # if insert_query != "":
        #     query(f"insert ignore into TagOf(VideoId, Tag) values " + insert_query[:-2])

if __name__ == "__main__":
    ts = time()
    update_video()

    print((time() - ts)/60)