# TwitterCrawl的使用示例

## 方法调用
```Python
from Crawler.Twitter_Crawl.TwitterCrawl import TwitterClass
keyword = '李子柒'
twittercrawl = TwitterClass()
response_data = twittercrawl.getResponse('Search',keyword)
entitylist = twittercrawl.GetEntitylist(response_data)
```

## 函数参数说明
### 1、getResponse(twitter_type,keyword)
- twitter_type:用于指定函数类别
- keyword：为传入的关键词
```Python 
Search、keyword：搜索功能，其中keyword代表关键词。每次默认返回搜索页人物列前20条
UserByScreenName、keyword：个人主页信息，其中keyword为用户的域名。返回用户信息
UserTweets、keyword：个人主页tweets列表信息，其中keyword为用户id。每次默认返回40条推文数据
TweetDetail、keyword：推文信息，其中keyword为推文id。返回第一条数据为推文信息，后续为评论信息
Following、keyword：用户关注列表，其中keyword为用户id。每次默认返回100条关注用户信息
```
### 2、TwitterUserInfo(result)
以李子柒为例https://twitter.com/cnliziqi
```Json
{
  "domain": "cnliziqi  域名，即@后面的名字，唯一标识",
  "screen_name": "李子柒  用户名",
  "description": "个人简介",
  "created_at": "Thu Aug 24 10:41:00 +0000 2017  创建时间",
  "id": "VXNlcjo5MDA2NjkyNjIyOTcxNTc2MzI=",
  "user_id": "900669262297157632  用户id",
  "location": "China",
  "verified": false, //(bool类型)
  "profile_image_url_https": "",
  "friends_count": "86375  粉丝数",
  "followers_count": "0 关注数",
  "statuses_count": "498  所有动态的总数",
  "media_count": "480  media列的总数",
  "tweets_count": "213  tweets列的总数",
  "expanded_url": "https://t.co/qXllCWxhCh  外部链接"
}
```
### 3、TwitterTweerInfo(result)
```Json
{
  "tweet_id": "推文id",
  "tweet_url": "推文链接",
  "created_at": "创建时间",
  "content_text": "文本内容",
  "content_picture": "图片内容链接",
  "content_video": "视频内容链接",
  "reply_count": "评论数",
  "retweet_count": "转发数",
  "quote_count": "引用数",
  "favorite_count": "点赞数",
  "bookmark_count": "标记数",
  "veiws_count": "浏览数",
  "user_id": "用户id",
  "user_domain": "用户域名",
  "user_screen_name": "用户名"
}
```