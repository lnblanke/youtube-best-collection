import json
from utils import query, get_request_body, get_connection
import yaml

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
    
        cnx = get_connection(yaml.safe_load(open("/opt/config.yaml"))["database"])
        cursor = cnx.cursor()
    
        cursor.callproc("top_ten_procedure", (CategoryId, Region, SelectedColumn.lower(), SortBy))
    
        outputs = []
    
        for result in cursor.stored_results():
            for [Id, title, viewcount, likes] in result.fetchall():
                outputs.append({
                    "Id": Id,
                    "Title": title,
                    "ViewCount": viewcount,
                    "Likes": likes
                })
                
        cursor.close()
    except Exception as e:
        error = e

    return get_request_body("GET", outputs, error)