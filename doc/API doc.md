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
| [isFavorite](#isFavorite)         | `GET`    |
| [searchVideo](#searchVideo)       | `GET`    |
| [sortTrending](#sortTrending)     | `GET`    |
| [topTen](#topTen)                 | `GET`    |
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
            "VideoId": "shZyg5VFI1Y",
            "Title": "YOASOBI「Biri-Biri」 Official Music Video"
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
    "Week": "2023-11-15"
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "VideoId": "b_l1IP_6psY",
            "Week": "2023-11-12 00:00:00",
            "Title": "Watch Out (Official Audio) Sidhu Moose Wala | Sikander Kahlon | Mxrci | Latest Punjabi Songs 2023",
            "ViewCount": 18728566,
            "Likes": 2276771
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
            "value": "2023-10-15"
        }
    ]
  }
  ```

#### isFavorite
- Description
  Given `UserId` and `VideoId`, check whether the user has a favorite video with `VideoId`
- Type: `GET`
- Sample request body
  ```json
  {
    "VideoId": "shZyg5VFI1Y",
    "UserId": "2"
  }
  ```
- Sample response body
  ```json
  {
    "data": true
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
    "CategoryId": 2,  [Not required]
    "Region": "JP",  [Not required]
    "SortBy": "relevance",  [Likes | ViewCount | PublishedAt | TrendingDate | Relevance]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "VideoId": "shZyg5VFI1Y",
            "Relevance": 12,
            "Title": "YOASOBI「Biri-Biri」 Official Music Video",
            "PublishedAt": "2023-11-18 13:00:09",
            "Likes": 135773,
            "TrendingDate": "2023-11-19 00:00:00",
            "ViewCount": 1859377,
            "ThumbnailLink": "https://i.ytimg.com/vi/shZyg5VFI1Y/default.jpg",
            "LikesChange": 135773,
            "ViewCountChange": 1859377,
            "ChannelId": "UCvpredjG93ifbCP1Y77JyFA",
            "ChannelTitle": "Ayase / YOASOBI",
            "CategoryId": 2,
            "CategoryTitle": "Music"
        },
        {
            "VideoId": "0N5r5VEppio",
            "Relevance": 5,
            "Title": "[뮤뱅 원테이크] 스트레이 키즈 (Stray Kids) '락 (樂) (LALALALA)' Bonus Ver. @뮤직뱅크 (Music Bank) 231110",
            "PublishedAt": "2023-11-10 10:00:01",
            "Likes": 92888,
            "TrendingDate": "2023-11-18 00:00:00",
            "ViewCount": 1062804,
            "ThumbnailLink": "https://i.ytimg.com/vi/0N5r5VEppio/default.jpg",
            "LikesChange": 11611,
            "ViewCountChange": 132851,
            "ChannelId": "UCeLPm9yH_a_QH8n6445G-Ow",
            "ChannelTitle": "KBS Kpop",
            "CategoryId": 2,
            "CategoryTitle": "Music"
        },
        {
            "VideoId": "3FuSyMhwiNs",
            "Relevance": 5,
            "Title": "[예능연구소] NiziU - HEARTRIS(니쥬 – 하트리스) FanCam | Show! MusicCore | MBC231111방송",
            "PublishedAt": "2023-11-11 10:38:29",
            "Likes": 12430,
            "TrendingDate": "2023-11-18 00:00:00",
            "ViewCount": 393078,
            "ThumbnailLink": "https://i.ytimg.com/vi/3FuSyMhwiNs/default.jpg",
            "LikesChange": 1776,
            "ViewCountChange": 56154,
            "ChannelId": "UCe52oeb7Xv_KaJsEzcKXJJg",
            "ChannelTitle": "MBCkpop",
            "CategoryId": 2,
            "CategoryTitle": "Music"
        },
        {
            "VideoId": "CUSUhXqThjY",
            "Relevance": 5,
            "Title": "Aimer「白色蜉蝣」 Music Video",
            "PublishedAt": "2023-11-14 12:00:11",
            "Likes": 14532,
            "TrendingDate": "2023-11-19 00:00:00",
            "ViewCount": 384616,
            "ThumbnailLink": "https://i.ytimg.com/vi/CUSUhXqThjY/default.jpg",
            "LikesChange": 2906,
            "ViewCountChange": 76923,
            "ChannelId": "UCR1zT1s524Hbc85bdvno_8w",
            "ChannelTitle": "Aimer Official YouTube Channel",
            "CategoryId": 2,
            "CategoryTitle": "Music"
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
    "CategoryId": 0, [Not required]
    "Region": "JP", [Not required]
    "ChannelId": "", [Not required]
    "SortBy": "likes",  [Likes | ViewCount | PublishedAt | TrendingDate]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "VideoId": "chIqaTzttWE",
            "Region": [
                "JP"
            ],
            "Title": "【大公開】くろのわのマネージャーってどんな仕事してるの？  #くろなん",
            "PublishedAt": "2023-11-13 10:00:08",
            "Likes": 19932,
            "TrendingDate": "2023-11-24 00:00:00",
            "ViewCount": 501009,
            "ThumbnailLink": "https://i.ytimg.com/vi/chIqaTzttWE/default.jpg",
            "LikesChange": 168,
            "ViewCountChange": 7783,
            "ChannelId": "UCz6vnIbgiqFT9xUcD6Bp65Q",
            "ChannelTitle": "ChroNoiR",
            "CategoryId": 0,
            "CategoryTitle": "Film & Animation"
        },
        {
            "VideoId": "kEc6IegVHas",
            "Region": [
                "JP"
            ],
            "Title": "劇場版『機動戦士ガンダムSEED FREEDOM』第4弾PV",
            "PublishedAt": "2023-11-19 10:30:16",
            "Likes": 13592,
            "TrendingDate": "2023-11-24 00:00:00",
            "ViewCount": 1016623,
            "ThumbnailLink": "https://i.ytimg.com/vi/kEc6IegVHas/default.jpg",
            "LikesChange": 334,
            "ViewCountChange": 73062,
            "ChannelId": "UC7wu64jFsV02bbu6UHUd7JA",
            "ChannelTitle": "ガンダムチャンネル",
            "CategoryId": 0,
            "CategoryTitle": "Film & Animation"
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
    "CategoryId": 0,
    "Region": "JP",
    "SortBy": "likes" [Likes | ViewCount]
  }
  ```
- Sample response body
  ```json
  {
    "data": [
        {
            "Id": "chIqaTzttWE",
            "Title": "【大公開】くろのわのマネージャーってどんな仕事してるの？  #くろなん",
            "ViewCount": 484380,
            "Likes": 19524
        },
        {
            "Id": "vvuD5bPYimU",
            "Title": "映画『ゴジラ-1.0』公開記念特番 Behind the scenes -No.30-ト云フモノ",
            "ViewCount": 902955,
            "Likes": 10903
        },
        {
            "Id": "bgvNjZ7uvOU",
            "Title": "映画『首』 90秒予告編",
            "ViewCount": 259698,
            "Likes": 565
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
