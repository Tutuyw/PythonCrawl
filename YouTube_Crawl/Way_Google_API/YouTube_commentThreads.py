import pymongo

from Crawler.Common_Def.common_request_url import request_url_json

# api_key = 'AIzaSyDmU-iYzIEu73OU3Bie_xkVmIir-wAU23M'
api_key = 'AIzaSyDmU-iYzIEu73OU3Bie_xkVmIir-wAU23M'
api_url = 'https://www.googleapis.com/youtube/v3/'
headers = {
    'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

conn = pymongo.MongoClient('mongodb://root:Bigdata#2021@175.27.160.162:27017/')
database = conn['media_resp']
collection_read = database['litaiyuan_youtube']
collection_save = database['litaiyuan_youtube_comment']

def get_commentThreads(vid):
    global commentThreads_url
    commentThreads_para = {
        'type': 'commentThreads',
        'id_type': f'videoId={vid}',
        'part': 'snippet'
    }
    type = commentThreads_para['type']
    id_type =commentThreads_para['id_type']
    part = commentThreads_para['part']
    # time、relevance
    order = 'time'
    commentThreads_url = f'{api_url}{type}?key={api_key}&part={part}&{id_type}&order={order}&maxResults=100&textFormat=plainText'
    commentThreads_data = request_url_json(commentThreads_url, headers)
    # print(commentThreads_data)
    judge_nextPageToken(commentThreads_data,commentThreads_url)

def get_comment(pid):
    global comment_url
    comment_para = {
        'type': 'comments',
        'id_type': f'parentId={pid}',
        'part': 'snippet'
    }
    type = comment_para['type']
    id_type =comment_para['id_type']
    part = comment_para['part']
    # time、relevance
    order = 'time'
    comment_url = f'{api_url}{type}?key={api_key}&part={part}&{id_type}&order={order}&maxResults=100&textFormat=plainText'
    response_data = request_url_json(comment_url, headers)
    # print(response_data)
    judge_nextPageToken(response_data,comment_url)

def judge_nextPageToken(response_data,req_url):
    if 'nextPageToken' in response_data.keys():
        nextPageToken = response_data['nextPageToken']
        print(nextPageToken)
        if 'commentThreads' in req_url:
            get_commentThreads_info(response_data)
            # print('下一页',nextPageToken)
            get_nextPageToken(commentThreads_url, nextPageToken)
        elif 'comments' in req_url:
            get_comments_info(response_data)
            # print('下一页', nextPageToken)
            get_nextPageToken(comment_url, nextPageToken)
    else:
        if 'commentThreads' in req_url:
            get_commentThreads_info(response_data)
        elif 'comments' in req_url:
            get_comments_info(response_data)

def get_commentThreads_info(response_data):
    for commentThread in response_data['items']:
        commentThread_mes = {}
        commentThread_mes['_id'] = commentThread['id']
        commentThread_mes['vid'] = vid
        commentThread_mes['author'] = commentThread['snippet']['topLevelComment']['snippet']['authorDisplayName']
        publishedTime = commentThread['snippet']['topLevelComment']['snippet']['publishedAt']
        updatedTime = commentThread['snippet']['topLevelComment']['snippet']['updatedAt']
        commentThread_mes['time'] = updatedTime
        textOriginal = commentThread['snippet']['topLevelComment']['snippet']['textOriginal'].replace('\n','')
        commentThread_mes['content'] = commentThread['snippet']['topLevelComment']['snippet']['textOriginal']
        commentThread_mes['comment_data'] = commentThread
        commentThread_mes['vertify'] = False
        reply_num = commentThread['snippet']['totalReplyCount']
        try:
            if collection_save.find_one({'_id':commentThread_mes['_id']}) == None:
                collection_save.insert_one(commentThread_mes)
        except Exception as e:
            print(e,'\n',commentThread_mes)
            # collection.update_one(commentThread_mes)

        # print(commentThread_mes['_id'],reply_num)
        if reply_num != 0:
            pid = commentThread_mes['_id']
            # print('进入次评论')
            get_comment(pid)

def get_comments_info(response_data):
    for comment in response_data['items']:
        # print(comment)
        comment_mes = {}
        comment_mes['_id'] = comment['id']
        comment_mes['vid'] = vid
        comment_mes['author'] = comment['snippet']['authorDisplayName']
        publishedTime = comment['snippet']['publishedAt']
        updatedTime = comment['snippet']['updatedAt']
        comment_mes['time'] = updatedTime
        comment_mes['content'] = comment['snippet']['textOriginal']
        comment_mes['channel'] = comment['snippet']['authorChannelId']['value']
        comment_mes['parentId'] = comment['snippet']['parentId']
        comment_mes['vertify'] = False
        # print(comment_mes['_id'])
        try:
            if collection_save.find_one({'_id':comment_mes['_id']}) == None:
                collection_save.insert_one(comment_mes)
        except Exception as e:
            print(e,'\n',comment_mes)
            # collection.update_one(comment_mes)

def get_nextPageToken(req_url,nextPageToken):
    nextPageToken_url = f'{req_url}&pageToken={nextPageToken}'
    response_data = request_url_json(nextPageToken_url, headers)
    # print(response_data)
    judge_nextPageToken(response_data,nextPageToken_url)

# 解决：maximum recursion depth exceeded in comparison
# import sys
# sys.setrecursionlimit(100000) #例如这里设置为十万
official_list = ['mBwVtL-gJUU','5jIiGZPWqK0','IRMLmx_luF8','o57BE57_wis','PIO9j-kohrk','I_zYC1JoCRs','2NEFatam-Ko','iwNgg8iAFoA',
                 'BWF0SFt7zCQ','oM-wbNHqsIk','tXZEmkE0d6A','3tBmQzai-eo','xE-zjPEPRV0','sCVekzHMteI','KedNwowodrQ','IFOqch8vEJU']
notofficial = [
    #'EnD1DfT7JQs','sG9H6dikI2w','zagdDghnP9g','tDoju-EfUEA',
               'neML4Orm5Ww','FZqB4btqiDc','ZAf79dF2dq0','FcLHjKK5EXA',
               '6HImwkywyT4','AVGe0pGpu74','Lac00ka-5rA','AE-f4_KwmWE','U3zmxI_gKBQ','BKPO-kd1hAM','MjLFGBNJUPM','qxPLiuVR1S4']
# for item in notofficial:
global vid
vid = 'sG9H6dikI2w'
print(vid)
get_commentThreads(vid)

# print(collection_save.find_one({'_id':'UgwsKiBdXhGR84iFIwh4AaABA'}))