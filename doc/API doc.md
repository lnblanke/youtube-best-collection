# YouTube API document

### Status Codes

| Status code | Description                                            |
| ----------- | ------------------------------------------------------ |
| 200         | Success                                                |
| 201         | Created                                                |
| 400         | Bad request (check error message for more info)        |
| 403         | Forbidden (possibly missing API key)                   |
| 502         | Bad gateway (possible bug in backend so please report) |

### CORS

All APIs listed in the table have enabled cross-origin resource sharing(CORS) and can be accessed from any origin with API key.

### Request head

```json
{
    "x-api-key": $API KEY$
}
```

### Request body
For illustration purposes, we listed request body for each `GET` request method. However, in development this should be changed to query string type. For example,
```json
  {
    "Region": "JP",
    "CategoryId": 10
  }
```
should be changed to:
```
base_url/endpoint?Region=JP&CategoryId=10
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

Development environment: `https://6cbpmuhemh.execute-api.us-east-2.amazonaws.com/dev/`

Production environment: `https://6cbpmuhemh.execute-api.us-east-2.amazonaws.com/prod/`

### Conventions

- Request and response bodies are encoded in JSON
- Property names are in CamelCase

### List of API endpoints

| Endpoint                          | Method   |
| --------------------------------- | -------- |
| [changeUserInfo](#changeuserinfo) | `PUT`    |
| [favoriteDelete](#favoriteDelete) | `DELETE` |
| [favoriteInsert](#favoriteInsert) | `POST`   |
| [getCategory](#getCategory)       | `GET`    |
| [getFavorite](#getFavorite)       | `GET`    |
| [getUserInfo](#getUserInfo)       | `GET`    |
| [getWeeklyBest](#getWeeklyBest)   | `GET`    |
| [getWeeks](#getWeeks)             | `GET`    |
| [sortTrending](#sortTrending)     | `GET`    |
| [topTen](#topTen)                 | `GET`    |
| [searchVideo](#searchVideo)       | `GET`    |
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

#### getCategory

- Description

  Get all categories
- Type: `GET`
- Sample request body
  ```json
  {
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "CategoryId": 1,
            "CategoryTitle": "Film & Animation"
        }
    ]
  }
  ```

#### getFavorite

- Description
  
  Get all favorite videos for a given `UserId`
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
        {
            "VideoId": "_-uDBzkV1dI",
            "UserId": 2,
            "Region": "KR",
            "Title": "시공하기 좋은 날 하늘궁전 업ㄱ레이드☆",
            "PublishedAt": "2023-08-29 10:36:48",
            "Likes": 3359,
            "TrendingDate": "2023-08-30 00:00:00",
            "ViewCount": 120353,
            "ThumbnailLink": "https://i.ytimg.com/vi/_-uDBzkV1dI/default.jpg",
            "LikesChange": 3359,
            "ViewCountChange": 120353,
            "ChannelId": "UCsHXnEd4VtCcKC0SN6ajBGA",
            "CategoryId": 24
        },
        {
            "VideoId": "z-_vxDY1Gu0",
            "UserId": 2,
            "Region": "JP",
            "Title": "【超学生×四季凪アキラ】威風堂々 @歌ってみた",
            "PublishedAt": "2023-10-12 10:00:09",
            "Likes": 46311,
            "TrendingDate": "2023-10-16 00:00:00",
            "ViewCount": 462352,
            "ThumbnailLink": "https://i.ytimg.com/vi/z-_vxDY1Gu0/default.jpg",
            "LikesChange": 46311,
            "ViewCountChange": 462352,
            "ChannelId": "UCxIK6x6sG7Ln5vjjPYpgeAw",
            "CategoryId": 10
        }
    ]
  }
  ```

#### getUserInfo 

- Description

  Get user info for given `UserName` 
- Type: `GET`
- Sample request body
  ```json
  {
    "UserName": "114514"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "UserId": 2,
            "Password": "bbbbronya",
            "UserName": "114514",
            "Gender": "Male",
            "Avatar": null
        }
    ]
  }
  ```

#### getWeeklyBest

- Description

  Get weekly best videos for the Week of `Week`
- Type: `GET`
- Sample request body
  ```json
  {
    "Week": "2023-10-19 11:45:14"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "VideoId": "r105CzDvoo0",
            "Week": "2023-10-15 00:00:00",
            "Region": "JP",
            "Title": "milet「Anytime Anywhere」MUSIC VIDEO (TVアニメ『葬送のフリーレン』エンディングテーマ)",
            "PublishedAt": "2023-10-06 13:00:09",
            "Likes": 30032,
            "TrendingDate": "2023-10-16 00:00:00",
            "ViewCount": 3117784,
            "ThumbnailLink": "https://i.ytimg.com/vi/r105CzDvoo0/default.jpg",
            "LikesChange": 30032,
            "ViewCountChange": 3117784,
            "ChannelId": "UCpgxgkifUGSKg9dNFE5Vo7Q",
            "CategoryId": 10
        }
    ]
  }
  ```

#### getWeeks

- Description
  Get all weeks with weekly best
- Type: `GET`
- Sample request body
  ```json
  {
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "value": "2023-10-15 00:00:00"
        }
    ]
  }
  ```

#### searchVideo

- Description
  
  Search for trending videos based on `Prompt`, sorted by `Likes`, `ViewCount`, `PublishedAt`, `TrendindDate`, or `Relevence` and filtered by `CategoryId` and/or `Region`. 
- Type: `GET`
- Sample request body
  ```json
  {
    "Prompt": "YOASOBI anime music",
    "CategoryId": 10,  [Not required]
    "Region": "JP",  [Not required]
    "SortBy": "relevance",  [Likes | ViewCount | PublishedAt | TrendingDate | Relevance]
    "PageNum": 0, [Not required, default: 0]
    "VideoPerPage": 5  [Not required, default: 20]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "VideoId": "HPtq8YK8fDQ",
            "Relevance": "1.6556",
            "Region": "JP",
            "Title": "青のすみか (Live in Blue) / キタニタツヤ - Where Our Blue Is (Live in Blue) / Tatsuya Kitani",
            "PublishedAt": "2023-08-24 12:00:08",
            "Likes": 20233,
            "TrendingDate": "2023-08-30 00:00:00",
            "ViewCount": 405200,
            "ThumbnailLink": "https://i.ytimg.com/vi/HPtq8YK8fDQ/default.jpg",
            "LikesChange": 20233,
            "ViewCountChange": 405200,
            "ChannelId": "UCgP3GbgbuVzAhlctGU5yuPA",
            "CategoryId": 10
        },
        {
            "VideoId": "-QKk9pKCufs",
            "Relevance": "0.9768",
            "Region": "JP",
            "Title": "【未公開映像】EXPO Behind the scenes vol.1 ｜NHK MUSIC EXPO 2023 | NHK",
            "PublishedAt": "2023-09-14 03:56:38",
            "Likes": 10984,
            "TrendingDate": "2023-09-15 00:00:00",
            "ViewCount": 214928,
            "ThumbnailLink": "https://i.ytimg.com/vi/-QKk9pKCufs/default.jpg",
            "LikesChange": 10984,
            "ViewCountChange": 214928,
            "ChannelId": "UC8T8_deSUS97DWZeKO_TL9Q",
            "CategoryId": 10
        },
        {
            "VideoId": "1z-_XtdtMwk",
            "Relevance": "0.9768",
            "Region": "JP",
            "Title": "Sexy Zone ｢本音と建前｣ (YouTube Ver.)",
            "PublishedAt": "2023-08-23 12:00:12",
            "Likes": 0,
            "TrendingDate": "2023-08-30 00:00:00",
            "ViewCount": 1327522,
            "ThumbnailLink": "https://i.ytimg.com/vi/1z-_XtdtMwk/default.jpg",
            "LikesChange": 0,
            "ViewCountChange": 1327522,
            "ChannelId": "UCgXJMvOBqHk5wJFRKZfIgWQ",
            "CategoryId": 10
        },
        {
            "VideoId": "DxyZt6CqGe0",
            "Relevance": "0.9768",
            "Region": "JP",
            "Title": "Sexy Zone「本音と建前」@CDTV ライブ! ライブ!",
            "PublishedAt": "2023-10-04 03:00:06",
            "Likes": 0,
            "TrendingDate": "2023-10-14 00:00:00",
            "ViewCount": 609122,
            "ThumbnailLink": "https://i.ytimg.com/vi/DxyZt6CqGe0/default.jpg",
            "LikesChange": 0,
            "ViewCountChange": 609122,
            "ChannelId": "UCgXJMvOBqHk5wJFRKZfIgWQ",
            "CategoryId": 10
        },
        {
            "VideoId": "mctEybOqY6s",
            "Relevance": "0.9768",
            "Region": "JP",
            "Title": "勇者",
            "PublishedAt": "2023-09-28 10:00:44",
            "Likes": 17060,
            "TrendingDate": "2023-09-29 00:00:00",
            "ViewCount": 268215,
            "ThumbnailLink": "https://i.ytimg.com/vi/mctEybOqY6s/default.jpg",
            "LikesChange": 17060,
            "ViewCountChange": 268215,
            "ChannelId": "UCI6B8NkZKqlFWoiC_xE-hzA",
            "CategoryId": 10
        }
    ]
  }
  ```

#### sortTrending

- Description
  
  Sort trending videos from past week by `Likes`, `ViewCount`, `PublishedAt`, or `TrendingDate` and filter by `CategoryId`, `Region`, and/or `ChannelId`. 
- Type: `GET`
- Sample request body
  ```json
  {
    "CategoryId": 20, [Not required]
    "Region": "JP", [Not required]
    "ChannelId": "UCAVR6Q0YgYa8xwz8rdg9Mrg", [Not required]
    "SortBy": "likes",  [Likes | ViewCount | PublishedAt | TrendingDate]
    "PageNum": 0,  [Not required, default: 0]
    "VideoPerPage": 10  [Not required, default: 20]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "VideoId": "U5VJ2RMwRAY",
            "Region": "JP",
            "Title": "【原神】キャラクター実戦紹介　フリーナ(CV：水瀬いのり)「世界はみな舞台」",
            "PublishedAt": "2023-11-07 04:00:10",
            "Likes": 102566,
            "TrendingDate": "2023-11-08 00:00:00",
            "ViewCount": 1441686,
            "ThumbnailLink": "https://i.ytimg.com/vi/U5VJ2RMwRAY/default.jpg",
            "LikesChange": 102566,
            "ViewCountChange": 1441686,
            "ChannelId": "UCAVR6Q0YgYa8xwz8rdg9Mrg",
            "CategoryId": 20
        }
    ]
  }
  ```

#### topTen

- Description
  
  Get top ten `Video` or `Channel` based on `CategoryId` and `Region` for today
- Type: `GET`
- Sample request body
  ```json
  {
    "SelectedColumn": "Title", [Title | ChannelTitle]
    "CategoryId": 20,
    "Region": "JP",
    "SortBy": "likes" [Likes | ViewCount]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "Title": "【阿鼻叫喚】鼻毛綱引きで最強の男を決めろ！？！？",
            "ViewCount": 149143,
            "Likes": 12776
        },
        {
            "Title": "神域リーグ2023 エキシビションマッチ",
            "ViewCount": 280960,
            "Likes": 4754
        },
        {
            "Title": "【原神】新星5キャラ　フリーナ解説　全体ダメージバフ持ちの神サポート！【げんしん】",
            "ViewCount": 256720,
            "Likes": 4065
        },
        {
            "Title": "VALORANT - CRカップ顔合わせよりもスクリムよりもなぜかキリンに夢中なチームがあるらしい w/ 獅子堂あかり 善悪菌 VanilLa ボドカ 夢野あかり",
            "ViewCount": 184904,
            "Likes": 3586
        }
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
