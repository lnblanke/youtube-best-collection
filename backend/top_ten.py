import json
from utils import query, get_request_body

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        req = event["queryStringParameters"]
        SelectedColumn = req.get("SelectedColumn")
        CategoryId = req.get("CategoryId")
        Region =  req.get("Region")
        SortBy = req.get("SortBy")
    
        assert CategoryId is not None, "CategoryId is empty"
        assert Region is not None, "Region is empty"
        assert SelectedColumn.lower() in ['title', 'channeltitle'], f"Invalid select column: {SelectedColumn}"
        assert SortBy.lower() in ['viewcount', 'likes'], f"Invalid sort column: {SortBy}"
        
        category = query(f"select CategoryId from Category where CategoryId = {CategoryId}")
        assert len(category) > 0, "Category with CategoryId does not exist"
        
        region = query(f"select Region from Video where Region = '{Region}'")
        assert len(region) > 0, "Region does not exist"
        
        if SelectedColumn.lower() == "title":
            SelectedColumn = "VideoId, Title"
        else:
            SelectedColumn = "ChannelId, ChannelTitle"
    
        result = query(f"select {SelectedColumn}, ViewCount, Likes from Video natural join Channel where CategoryId = '{CategoryId}' and Region = '{Region}' and TrendingDate = (select max(TrendingDate) from Video) group by {SelectedColumn} order by {SortBy} DESC limit 10")
    
        outputs = []
    
        for [Id, title, viewcount, likes] in result:
            outputs.append({
                "Id": Id,
                "Title": title,
                "ViewCount": viewcount,
                "Likes": likes
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)