import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])

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
                list_tags.append(f"\'{' '.join(prompt[i: j + 1])}\'")

        tags = query(f"select Tag from Tag where Tag in ({', '.join(list_tags)})")
        tags = [f"'{tag[0]}'" for tag in tags]

        sql = f"select * from (select VideoId, count(distinct Tag) as Relevence from TagOf to2 where Tag in ({', '.join(tags)}) group by VideoId) as t1 natural join Video"

        assert SortBy.lower() in ['viewcount', 'likes', 'relevence', 'publishedat', 'trendingdate'], f"Invalid sort column: {SortBy}"
    
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

        return {
          "isBase64Encoded" : True,
          "statusCode": 200,
          "headers": {},
          "body": json.dumps({
              "data": result
          }, default = str)
        }
    except Exception as e:
        return {
          "isBase64Encoded" : True,
          "statusCode": 400,
          "headers": {},
          "body": json.dumps({
              "error_message": str(e)
          })
        }