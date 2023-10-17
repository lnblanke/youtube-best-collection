# YouTube API document

### Status Codes

| Status code | Description                                            |
| ----------- | ------------------------------------------------------ |
| 200         | Success                                                |
| 201         | Created                                                |
| 400         | Bad request (check error message for more info)        |
| 403         | Forbidden (possibly missing API key)                   |
| 502         | Bad gateway (possible bug in backend so please report) |

### Request head

```json
{
    "x-api-key": $API KEY$
}
```

### Base URL

`https://6cbpmuhemh.execute-api.us-east-2.amazonaws.com/dev/`

### Conventions

- Request and response bodies are encoded in JSON
- Property names are in CamelCase

### List of API endpoints

#### favoriteDelete

- Description
  
  Delete from `Favorite` based on `UserId` and `VideoId`
- Type: `DELETE`
- Sample request body
  ```json
  {
    "VideoId": "z-_vxDY1Gu0",
    "UserId": "2"
  }
  ```
- Sample response body
  ```json
  {
    "message": "success"
  }
  ```

#### favoriteInsert

- Description
  
  Insert into `Favorite` with value of `UserId` and `VideoId`
- Type: `POST`
- Sample request body
  ```json
  {
    "VideoId": "z-_vxDY1Gu0",
    "UserId": "2"
  }
  ```
- Sample response body
  ```json
  {
    "message": "success"
  }
  ```

#### sortTrending
- Description
  
  Sort and filter trending videos based on criteria
- Type: `GET`
- Sample request body
  ```json
  {
    "CategoryId": 10,
    "Region": "JP",
    "ChannelId": "UCxIK6x6sG7Ln5vjjPYpgeAw",
    "SortBy": "likes"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            "z-_vxDY1Gu0",
            "JP",
            "【超学生×四季凪アキラ】威風堂々 @歌ってみた",
            "2023-10-12 10:00:09",
            32155,
            "2023-10-13 00:00:00",
            240720,
            "https://i.ytimg.com/vi/z-_vxDY1Gu0/default.jpg",
            32155,
            240720,
            "UCxIK6x6sG7Ln5vjjPYpgeAw",
            10
        ]
    ]
  }
  ```

#### topTen
- Description
  
  Get top ten `VideoId` or `ChannelId` based on `CategoryId` and `Region` for today
- Type: `GET`
- Sample request body
  ```json
  {
    "SelectedColumn": "VideoId",
    "CategoryId": 10,
    "Region": "JP",
    "SortBy": "likes"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            "SR89b0qqRAg"
        ],
        [
            "WKRoCuL9pgA"
        ],
        [
            "wdm2t8pTp7Y"
        ]
    ]
  }
  ```

#### videoQuery
- Description
  
  Get top 50 videos for `Region` sorted by `ViewCount` or `Likes` from the past week
- Type: `GET`
- Sample request body
  ```json
  {
    "Region": "JP",
    "SortBy": "likes"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            "zS1jKIsAOmM",
            "JP",
            "NCT U 'The BAT' Archiving Video",
            "2023-08-29 14:38:57",
            140133,
            "2023-08-30 00:00:00",
            677026,
            "https://i.ytimg.com/vi/zS1jKIsAOmM/default.jpg",
            140133,
            677026,
            "UCwgtORdDtUKhpjE1VBv6XfA",
            10
        ],
        [
            "OIBODIPC_8Y",
            "JP",
            "YOASOBI「勇者」 Official Music Video／TVアニメ『葬送のフリーレン』オープニングテーマ",
            "2023-09-29 14:00:07",
            132074,
            "2023-09-30 00:00:00",
            1738367,
            "https://i.ytimg.com/vi/OIBODIPC_8Y/default.jpg",
            132074,
            1738367,
            "UCvpredjG93ifbCP1Y77JyFA",
            10
        ]
    ]
  }
  ```