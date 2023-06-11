import json
import re

import pymongo
import requests

from Crawler.Common_Def.common_request_url import request_url_json

api_key = 'AIzaSyCy2FikEJlwu6ef_lSbAFs-up1qbm4CyH8'
api_url = 'https://www.googleapis.com/youtube/v3/'
headers = {
    'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

conn = pymongo.MongoClient('mongodb://root:Bigdata#2021@175.27.160.162:27017/')
database = conn['media_resp']
collection = database['litaiyuan_youtube']


index = 0
def get_search(keyword):
    global youtube_search_url
    type = 'video'
    youtube_search_url = f'{api_url}search?key={api_key}&q={keyword}&type={type}&order=viewCount' \
                         f'&publishedAfter=2022-10-15T00:00:00Z&publishedBefore=2023-02-01T00:00:00Z&maxResults=50&part=snippet'
    response_data = request_url_json(youtube_search_url, headers)
    get_video_id(response_data)

"""
2022/10/15 -- 2022/10/28：Itaewon
2022/10/29 -- 2022/10/30：Itaewon Stampede\Itaewon\itaewon 1029\이태원
2022/10/31 -- 2022/11/12：Itaewon Stampede\이태원
2022/11/13 -- 2022/11/22：Itaewon Stampede\Itaewon\itaewon 1029\이태원
2022/11/23 -- 2022/12/12：Itaewon Stampede\Itaewon\itaewon 1029\이태원
2022/12/13 -- 2023/01/02：Itaewon Stampede\Itaewon\itaewon 1029\이태원
2023/01/03 --2023/01/12：Itaewon Stampede\Itaewon\itaewon 1029\이태원
2023/01/13 -- 2023/02/01：Itaewon Stampede\Itaewon\itaewon 1029\이태원
"""

def get_video_id(response_data):
    global index
    print(response_data)
    searchResult_items = response_data['items']
    for item in searchResult_items:
        videoId = item['id']['videoId']
        get_video_info(videoId)

    if 'nextPageToken' in response_data.keys() and index < 3:
        print('第',str(index),'页')
        index += 1
        nextPageToken = response_data['nextPageToken']
        get_nextPageToken(nextPageToken)
    else:
        print('没有下一页')

def get_nextPageToken(nextPageToken):
    nextPageToken_url = f'{youtube_search_url}&pageToken={nextPageToken}'
    response_data = request_url_json(nextPageToken_url, headers)
    get_video_id(response_data)

def get_video_info(videoId):
    video_url = f'{api_url}videos?key={api_key}&id={videoId}&part=snippet,statistics,contentDetails'
    response_data = request_url_json(video_url, headers)
    video_info = {}
    video_info['_id'] = response_data['items'][0]['id']
    video_info['author'] = response_data['items'][0]['snippet']['channelTitle']
    video_info['pubtime'] = response_data['items'][0]['snippet']['publishedAt']
    video_info['title'] = response_data['items'][0]['snippet']['title']
    video_info['description'] = response_data['items'][0]['snippet']['description']
    video_info['viewCount'] = response_data['items'][0]['statistics']['viewCount']
    try:
        video_info['likeCount'] = response_data['items'][0]['statistics']['likeCount']
    except:
        print('没有点赞：',video_info['_id'])
        video_info['likeCount'] = 0
    video_info['favoriteCount'] = response_data['items'][0]['statistics']['favoriteCount']
    try:
        video_info['commentCount'] = response_data['items'][0]['statistics']['commentCount']
    except:
        print('没有评论：',video_info['_id'])
        video_info['commentCount'] = 0
    video_info['keyword'] = '이태원'
    try:
        collection.insert_one(video_info)
    except Exception as e:
        print(e, '\n', video_info)

# Itaewon Stampede\Itaewon\itaewon 1029\이태원
get_search("이태원")
# get_video_info("XJWa1PqEPBg")
"""
2022/10/15
2022/10/29 韩国首尔龙山区梨泰院发生大规模踩踏事故
2022/10/30 韩国总统尹锡悦就首尔踩踏事故发表电视讲话，宣布全国哀悼
2022/11/13 梨泰院踩踏事故中的死亡人数升至158人，另有十人还在医院接受治疗。
2022/11/23 韩国国会宣布将启动“梨泰院踩踏事件”国政调查
2022/12/13 首尔梨泰院踩踏事故中幸存下来的一名青少年被发现死于自杀
2022/1/3 据韩联社报道，韩国首尔梨泰院踩踏事故遇难者人数升至159人
2022/1/13 韩国警察厅梨泰院事故特别调查本部发布了最终调查结果，公布事故原因
2023/2/1 
"""