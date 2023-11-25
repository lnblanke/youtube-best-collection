from utils import query, get_request_body

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        req = event["queryStringParameters"]

        assert req.get("Prompt") is not None, "Prompt is empty"

        if req.get("Prompt") == "":
            return get_request_body("GET", [], None)
        
        Prompt = req.get("Prompt").replace("\"", "\\\"").replace("\\", "\\\\").split(" ")
        CategoryId = req.get("CategoryId")
        Region = req.get("Region")
        SortBy = req.get("SortBy")

        assert SortBy is not None, "SortBy is not given"

        word_queries = []

        for word in Prompt:
            word_queries.append(f"(select distinct VideoId, {len(word)} as length from Video where Title like \"%{word}%\")")

        word_query = f"(select VideoId, sum(length) as Relevance from ({' union all '.join(word_queries)}) as t group by VideoId)"

        list_tags = []

        for i in range(len(Prompt)):
            for j in range(i, len(Prompt)):
                list_tags.append(f"\"{' '.join(Prompt[i: j + 1])}\"")

        tags = query(f"select Tag from Tag where Tag in ({', '.join(list_tags)})")
        tags = [f"\"{tag[0]}\"" for tag in tags]
        
        if len(tags) == 0:
            return get_request_body("GET", [], error)
        
        video_counts = query(f"select count(distinct VideoId) from TagOf where Tag in ({', '.join(tags)})")
        max_videos = max([count[0] for count in video_counts])
        num_videos = sum([count[0] for count in video_counts])

        tag_query = f"(select VideoId, sum(Importance) as Relevance from TagOf to2 natural join (select Tag, ({max_videos} - count(distinct VideoId)) / {num_videos} as Importance from TagOf group by Tag) as Factor where Tag in ({', '.join(tags)}) group by VideoId)"

        sql = f"select VideoId, Relevance, Title, PublishedAt, max(Likes), max(TrendingDate), max(ViewCount), ThumbnailLink, ChannelId, ChannelTitle, CategoryId, CategoryName, avg(LikesChange), avg(ViewCountChange) from (select VideoId, sum(Relevance) as Relevance from ({word_query} union all {tag_query}) as gp group by VideoId) as res natural join Video natural join Channel natural join Category "

        assert SortBy.lower() in ['viewcount', 'likes', 'relevance', 'publishedat', 'trendingdate'], f"Invalid sort column: {SortBy}"
    
        if CategoryId and CategoryId != "":
            sql += f" where CategoryId = {CategoryId}"
            
            category = query(f"select CategoryId from Category where CategoryId = {CategoryId}")
            assert len(category) > 0, "Category with CategoryId does not exist"
        if Region and Region != "":
            if CategoryId:
                sql += f" and Region = '{Region}'"
            else:
                sql += f" where Region = '{Region}'"
            
            region = query(f"select Region from Video where Region = '{Region}'")
            assert len(region) > 0, "Region does not exist"

        sql += f" group by VideoId, relevance, Title, PublishedAt, ThumbnailLink, ChannelId, CategoryId order by {SortBy} desc" 

        result = query(sql)
        
        outputs = []
        
        for [VideoId, Relevance, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, ChannelId, ChannelTitle, CategoryId, CategoryTitle, LikesChange, ViewCountChange] in result:
            outputs.append({
                "VideoId": VideoId,
                "Relevance": int(Relevance), 
                "Title": Title,
                "PublishedAt": PublishedAt,
                "Likes": Likes,
                "TrendingDate": TrendingDate,
                "ViewCount": ViewCount,
                "ThumbnailLink": ThumbnailLink,
                "LikesChange": int(LikesChange),
                "ViewCountChange": int(ViewCountChange),
                "ChannelId": ChannelId, 
                "ChannelTitle": ChannelTitle,
                "CategoryId": CategoryId,
                "CategoryTitle": CategoryTitle
            })
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)