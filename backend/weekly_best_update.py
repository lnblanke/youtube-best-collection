import json
from utils import query, get_request_body
import datetime
# population source: https://worldpopulationreview.com/, 2022. log tranformation applied.

def lambda_handler(event, context):
    outputs, error = None, None
    
    Week = "2023-11-12 00:00:00"
    
    try:

        region_weights = {'BR': 0.08, 'CA': 0.12, 'DE': 0.11, 'FR': 0.11, 'GB': 0.11, 'IN': 0.02, 'JP': 0.09, 'KR': 0.12, 'MX': 0.09, 'RU': 0.09, 'US': 0.06}

        sql_select = f"""SELECT VideoId, sum(TrendingCount * 1000000 * Weight) + 10 * sum(WeeklyLikesChange) / 11 + sum(WeeklyViewCountChange) / 11 as Score
                       FROM Video NATURAL JOIN RegionWeight 
                       WHERE TrendingCount > 0 AND VideoId NOT IN (select VideoId from WeeklyBest)
                       GROUP BY VideoId
                       ORDER BY Score DESC 
                       LIMIT 10"""

        videos = query(sql_select)

        for video in videos:
            video_id = video[0]
            sql_insert = f"INSERT INTO WeeklyBest (VideoId, Week) VALUES ('{video_id}', timestamp('{Week}'))"
            query(sql_insert)

    except Exception as e:
        error = e

    return get_request_body("PUT", None, error)


print(lambda_handler(None, None))





















    # VideoId出现过几次相当于Trending几次 (1) ，做当周的Trending次数，按地区人口加权
    



    # 1. 本周Trending 2. 之前以有数据：（ViewCount, Likes 除以 两次Trending的日期差
    # eg. (上周，因为这周没过完）最新日Trending, 如果有上上周数据，取最新（离上上周周日天数最小）的Trending，viewcount likes差值除以天数做平均值
    # 对于上周首次Trending，差值除以发布天数做平均值
    # 做view count和likes加权，比大小，筛选前十
    # Video里面会多俩average





