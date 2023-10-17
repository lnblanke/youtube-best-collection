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

### Response body
- `GET` success response body
  ```json
  {
    "data": [data_item 1, data_item 2, ...]
  }
  ```
- Other success response body
  ```json
  {
    "message": "success"
  }
  ```
- Failed response body
  ```json
  {
    "error_message": "error message"
  }
  ```

### Base URL

`https://6cbpmuhemh.execute-api.us-east-2.amazonaws.com/dev/`

### Conventions

- Request and response bodies are encoded in JSON
- Property names are in CamelCase

### List of API endpoints

| Endpoint                          | Method   |
| --------------------------------- | -------- |
| [changeUserInfo](#changeuserinfo) | `PUT`    |
| [favoriteDelete](#favoriteDelete) | `DELETE` |
| [favoriteInsert](#favoriteInsert) | `POST`   |
| [getFavorite](#getFavorite)       | `GET`    |
| [getUserInfo](#getUserInfo)       | `GET`    |
| [getWeeklyBest](#getWeeklyBest)   | `GET`    |
| [sortTrending](#sortTrending)     | `GET`    |
| [topTen](#topTen)                 | `GET`    |
| [searchVideo](#searchVideo)       | `GET`    |
| [updateVideo](#updateVideo)       | `PUT`    |
| [userInsert](#userInsert)         | `POST`   |

#### changeUserInfo

- Description
  
  Update user info with `UserId`
- Type: `PUT`
- Sample request body
  ```json
  {
    "UserId": 2,
    "Password": "bbbbronya", [Not required]
    "UserName": "114514", [Not required]
    "Gender": "Male", [Not required]
    "Avatar": "" [Not required]
  }
  ```
- Sample response body
  ```json
  {
    "message": "success"
  }
  ```

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

#### getFavorite

- Description
  
  Get all favorite videos for a given `UserId`
- Type: `GET`
- Sample request body
  ```json
  {
    "UserId": "3"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            "z-_vxDY1Gu0",
            3,
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

#### getUserInfo 

- Description

  Get user info for given `UserId` 
- Type: `GET`
- Sample request body
  ```json
  {
    "UserId": "2"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            2,
            "bbbbronya",
            "114514",
            "Male",
            null
        ]
    ]
  }
  ```

#### getWeeklyBest

- Description

  Get weekly best videos for a given `Week`
- Type: `GET`
- Sample request body
  ```json
  {
    "Week": "2023-10-15 00:00:00"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            "r105CzDvoo0",
            "2023-10-15 00:00:00",
            "JP",
            "milet「Anytime Anywhere」MUSIC VIDEO (TVアニメ『葬送のフリーレン』エンディングテーマ)",
            "2023-10-06 13:00:09",
            23182,
            "2023-10-11 00:00:00",
            1739109,
            "https://i.ytimg.com/vi/r105CzDvoo0/default.jpg",
            23182,
            1739109,
            "UCpgxgkifUGSKg9dNFE5Vo7Q",
            10
        ]
    ]
  }
  ```

#### sortTrending

- Description
  
  Sort trending videos from past week by `Likes` or `ViewCount` and filter by `CategoryId`, `Region`, and `ChannelId`. 
- Type: `GET`
- Sample request body
  ```json
  {
    "CategoryId": 10, [Not required]
    "Region": "JP", [Not required]
    "ChannelId": "UCpgxgkifUGSKg9dNFE5Vo7Q", [Not required]
    "SortBy": "likes",  [Likes or ViewCount]
    "PageNum": 0,  [Not required]
    "VideoPerPage": 10  [Not required]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            "r105CzDvoo0",
            "JP",
            "milet「Anytime Anywhere」MUSIC VIDEO (TVアニメ『葬送のフリーレン』エンディングテーマ)",
            "2023-10-06 13:00:09",
            23182,
            "2023-10-11 00:00:00",
            1739109,
            "https://i.ytimg.com/vi/r105CzDvoo0/default.jpg",
            23182,
            1739109,
            "UCpgxgkifUGSKg9dNFE5Vo7Q",
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
    "SelectedColumn": "Title", [Title or ChannelId]
    "CategoryId": 10,
    "Region": "JP",
    "SortBy": "likes" [Likes or ViewCount]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        [
            "SEKAI NO OWARI「最高到達点」ONE PIECE リリックMV"
        ],
        [
            "【号泣の最終回…】フランスストリートピアノの旅????????の最終日に愛の讃歌弾いたら…【海外ストリートピアノ/publicpiano/Hymne à l'amour/Édith Piaf】"
        ],
        [
            "King & Prince 「愛し生きること / MAGIC WORD」【初回限定盤A】「愛し生きること」 Music Video Shooting Behind the scenes Teaser"
        ]
    ]
  }
  ```

#### userInsert

- Description
  
  Insert into `UserInfo` with values of user info
- Type: `POST`
- Sample request body
  ```json
  {
    "Password": "wakuwaku",
    "UserName": "Aniya",
    "Gender": "Female", [Not required]
    "Avatar": "https://userpic.codeforces.org/318350/title/e053dcf9c9751cd7.jpg" [Not required]
  }
  ```
- Sample response body
  ```json
  {
    "message": "success"
  }
  ```
