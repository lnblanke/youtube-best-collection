import json
from sql_query import query

def lambda_handler(event, context):
    try:
        req = json.loads(event["body"])
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
    
        result = query(f"select {SelectedColumn} from Video natural join Channel where CategoryId = '{CategoryId}' and Region = '{Region}' and TrendingDate = (select max(TrendingDate) from Video) order by {SortBy} DESC limit 10")

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