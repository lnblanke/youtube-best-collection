from utils import query, get_request_body

def lambda_handler(event, context):
    outputs, error = None, None
    try:
        req = event["queryStringParameters"]

        assert req.get("Prompt") is not None, "Prompt is empty"

        if req.get("Prompt") == "":
            return get_request_body("GET", [], None)
        
        Prompt = req.get("Prompt") \
                    .replace("\"", "\\\"") \
                    .replace("{", "\\{") \
                    .replace("}", "\\}") \
                    .replace("[", "\\[") \
                    .replace("]", "\\]") \
                    .replace("(", "\\(") \
                    .replace(")", "\\)") \
                    .replace("^", "\\^") \
                    .replace("$", "\\$") \
                    .replace(".", "\\.") \
                    .replace("|", "\\|") \
                    .replace("?", "\\?") \
                    .replace("*", "\\*") \
                    .replace("+", "\\+") \
                    .replace("\\", "\\\\") \
                    .split(" ")
        CategoryId = req.get("CategoryId")
        ChannelId = req.get("ChannelId")
        Region = req.get("Region")
        SortBy = req.get("SortBy")

        assert SortBy is not None, "SortBy is not given"

        word_queries = []

        for word in Prompt:
            if word == "":
                continue
            
            word_queries.append(f"(select distinct VideoId, {len(word)} as length from Video where " + "regexp_like(Title, \"(^|(.*)[\\\\P{L}\\\\p{Hani}\\\\p{Kana}\\\\p{Hira}])" + word + "($|[\\\\P{L}\\\\p{Hani}\\\\p{Kana}\\\\p{Hira}].*)\"))")

        word_query = f"(select VideoId, sum(length) as Relevance from ({' union all '.join(word_queries)}) as t group by VideoId)"

        list_tags = []

        for i in range(len(Prompt)):
            for j in range(i, len(Prompt)):
                list_tags.append(f"\"{' '.join(Prompt[i: j + 1])}\"")

        tags = query(f"select Tag from Tag where Tag in ({', '.join(list_tags)})")
        tags = [f"\"{tag[0]}\"" for tag in tags]
        
        if len(tags) != 0:
            video_counts = query(f"select count(distinct VideoId) from TagOf where Tag in ({', '.join(tags)})")
            max_videos = max([count[0] for count in video_counts])
            num_videos = sum([count[0] for count in video_counts])
    
            tag_query = f"(select VideoId, sum(Importance) as Relevance from TagOf to2 natural join (select Tag, ({max_videos} - count(distinct VideoId)) / {num_videos} as Importance from TagOf group by Tag) as Factor where Tag in ({', '.join(tags)}) group by VideoId)"
        
            sql = f"select VideoId, Relevance, Title, PublishedAt, max(Likes), max(TrendingDate), max(ViewCount), ThumbnailLink, ChannelId, ChannelTitle, CategoryId, CategoryName, avg(LikesChange), avg(ViewCountChange) from (select VideoId, sum(Relevance) as Relevance from ({word_query} union all {tag_query}) as gp group by VideoId) as res natural join Video natural join Channel natural join Category "
        else:
            sql = f"select VideoId, Relevance, Title, PublishedAt, max(Likes), max(TrendingDate), max(ViewCount), ThumbnailLink, ChannelId, ChannelTitle, CategoryId, CategoryName, avg(LikesChange), avg(ViewCountChange) from (select VideoId, sum(Relevance) as Relevance from {word_query} as gp group by VideoId) as res natural join Video natural join Channel natural join Category "

        assert SortBy.lower() in ['viewcount', 'likes', 'relevance', 'publishedat', 'trendingdate'], f"Invalid sort column: {SortBy}"
    
        wheres = []
    
        if CategoryId and CategoryId != "":
            wheres.append(f"CategoryId = {CategoryId}")
            
            category = query(f"select CategoryId from Category where CategoryId = {CategoryId}")
            assert len(category) > 0, "Category with CategoryId does not exist"
        if Region and Region != "":
            wheres.append(f"Region = '{Region}'")
            
            region = query(f"select Region from Video where Region = '{Region}'")
            assert len(region) > 0, "Region does not exist"
        if ChannelId and ChannelId != "":
            wheres.append(f"ChannelId = '{ChannelId}'")
            
            region = query(f"select ChannelId from Channel where ChannelId = '{ChannelId}'")
            assert len(region) > 0, "Channel does not exist"
            
        if len(wheres) > 0:
            sql += f" where {' and '.join(wheres)}"

        sql += f" group by VideoId, ChannelId, CategoryId order by {SortBy} desc" 
        
        result = query(sql)
        
        outputs = []
        
        for [VideoId, Relevance, Title, PublishedAt, Likes, TrendingDate, ViewCount, ThumbnailLink, ChannelId, ChannelTitle, CategoryId, CategoryTitle, LikesChange, ViewCountChange] in result:
            outputs.append({
                "VideoId": VideoId,
                "Relevance": float(Relevance), 
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