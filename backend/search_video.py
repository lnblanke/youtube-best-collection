import json
from utils import query, get_request_body

def lambda_handler(event, context):
    result, error = None, None
    try:
        req = event["queryStringParameters"]

        assert req.get("Prompt") is not None, "Prompt is empty"
        
        prompt = [word.replace("\"", "'") for word in req.get("Prompt").split(" ")]
        CategoryId = req.get("CategoryId")
        Region =  req.get("Region")
        SortBy = req.get("SortBy")
        PageNum = req.get("PageNum")
        VideoPerPage = req.get("VideoPerPage")

        list_tags = []

        for i in range(len(prompt)):
            for j in range(i, len(prompt)):
                list_tags.append(f"\"{' '.join(prompt[i: j + 1])}\"")
                
        tags = query(f"select Tag from Tag where Tag in ({', '.join(list_tags)})")
        tags = [f"\"{tag[0]}\"" for tag in tags]
        
        if len(tags) == 0:
            return get_request_body("GET", [], error)
        
        video_counts = query(f"select count(distinct VideoId) from TagOf where Tag in ({', '.join(tags)})")
        max_videos = max([count[0] for count in video_counts])
        num_videos = sum([count[0] for count in video_counts])

        query(f"drop view if exists Factor")
        query(f"create view Factor as (select Tag, ({max_videos} - count(distinct VideoId)) / {num_videos} as Importance from TagOf group by Tag)")

        sql = f"select * from (select VideoId, sum(Importance) as Relevance from TagOf to2 natural join Factor where Tag in ({', '.join(tags)}) group by VideoId) as t1 natural join Video"

        assert SortBy.lower() in ['viewcount', 'likes', 'relevance', 'publishedat', 'trendingdate'], f"Invalid sort column: {SortBy}"
    
        if CategoryId:
            sql += f" where CategoryId = {CategoryId}"
            
            category = query(f"select CategoryId from Category where CategoryId = {CategoryId}")
            assert len(category) > 0, "Category with CategoryId does not exist"
        if Region:
            if CategoryId:
                sql += f" and Region = '{Region}'"
            else:
                sql += f" where Region = '{Region}'"
            
            region = query(f"select Region from Video where Region = '{Region}'")
            assert len(region) > 0, "Region does not exist"
        if VideoPerPage is None:
            VideoPerPage = 20
        if PageNum is None:
            PageNum = 0
        
        sql += f" ORDER BY {SortBy} DESC limit {VideoPerPage} offset {PageNum * VideoPerPage}" 

        result = query(sql)
    except Exception as e:
        error = e

    return get_request_body("GET", result, error)