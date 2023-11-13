import json
from utils import query, get_request_body
import datetime

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        req = event["queryStringParameters"]
        
        CategoryId = req.get("CategoryId")
        Region =  req.get("Region")
        ChannelId = req.get("ChannelId")
        SortBy = req.get("SortBy")
        PageNum = req.get("PageNum")
        VideoPerPage = req.get("VideoPerPage")
    
        cur = (datetime.datetime.now() - datetime.timedelta(days = 7)).strftime('%Y/%m/%d %H:%M:%S')
    
        sql = f"SELECT * from Video where TrendingDate >= timestamp(\"{cur}\")" 
        
        assert SortBy.lower() in ['viewcount', 'likes', 'publishedat', 'trendingdate'], f"Invalid sort column: {SortBy}"
    
        if CategoryId:
            sql += f" and CategoryId = {CategoryId}"
            
            category = query(f"select CategoryId from Category where CategoryId = {CategoryId}")
            assert len(category) > 0, "Category with CategoryId does not exist"
        if Region:
            sql += f" and Region = '{Region}'"
            
            region = query(f"select Region from Video where Region = '{Region}'")
            assert len(region) > 0, "Region does not exist"
        if ChannelId:
            sql += f" and ChannelId = '{ChannelId}'"
            
            channel = query(f"select ChannelId from Channel where ChannelId = '{ChannelId}'")
            assert len(channel) > 0, "Channel with ChannelId does not exist"
        if VideoPerPage is None:
            VideoPerPage = 20
        if PageNum is None:
            PageNum = 0
        
        sql += f" ORDER BY {SortBy} DESC limit {VideoPerPage} offset {int(PageNum) * int(VideoPerPage)}" 
    
        result = query(sql)
        
        outputs = []
        
        for [VideoId, Region, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, LikesChange, ViewCountChange, ChannelId, CategoryId] in result:
            outputs.append({
                "VideoId": VideoId,
                "Region": Region,
                "Title": Title,
                "PublishedAt": PublishedAt,
                "Likes": Likes,
                "TrendingDate": TrendingDate,
                "ViewCount": ViewCount,
                "ThumbnailLink": ThumbnailLink,
                "LikesChange": LikesChange,
                "ViewCountChange": ViewCountChange,
                "ChannelId": ChannelId, 
                "CategoryId": CategoryId
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)