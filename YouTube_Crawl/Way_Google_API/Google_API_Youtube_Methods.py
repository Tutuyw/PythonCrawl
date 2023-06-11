import json
import time

import requests

api_key = 'AIzaSyAvjIwPo9DPd2o9mbEobkVyzUFJ-cS2e5U'
api_url = 'https://www.googleapis.com/youtube/v3/'

# cnliziqi、
user_id = '李子柒Liziqi'
user_info_url = f'{api_url}channels?key={api_key}&forUsername={user_id}&part=snippet,contentDetails,statistics,topicDetails'

channel_id = 'UCoC47do520os_4DBMEFGg4A'
channel_info_url = f'{api_url}channels?key={api_key}&id={channel_id}&part=snippet,contentDetails,statistics,topicDetails'

vid = 'u-xS-dkz3a0'
video_info_search_url = f'{api_url}videos?key={api_key}&id={vid}&part=snippet,contentDetails,statistics,topicDetails'

test_url = f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername=GoogleDevelopers&key={api_key}'

q = '李子柒'
type = 'channel'
search_url = f'{api_url}search?key={api_key}&q={q}&type={type}&part=snippet,forContentOwner'

def get_youtube_search(username):
    type = 'channel'
    youtube_search_url = f'{api_url}search?key={api_key}&q={username}&type={type}&maxResults=5&part=snippet'
    response = requests.get(url=youtube_search_url)
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    response_data = json.loads(response.text)['items']
    for item in response_data:
        youtube_user_info = {}
        # https://www.youtube.com/channel/UCoC47do520os_4DBMEFGg4A
        youtube_user_info['screen_name'] = item['snippet']['title']
        youtube_user_info['channelId'] = item['snippet']['channelId']
        youtube_user_info['profile_image_url'] = item['snippet']['thumbnails']['default']['url']
        get_channel_url(youtube_user_info['channelId'],youtube_user_info)
        print(youtube_user_info)

def get_channel_url(channelId,youtube_user_info):
    time.sleep(5)
    channel_info_url = f'{api_url}channels?key={api_key}&id={channelId}&part=snippet,contentDetails,statistics,topicDetails'
    response = requests.get(url=channel_info_url)
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    response_data = json.loads(response.text)['items'][0]
    youtube_user_info['description'] = response_data['snippet']['description']
    try:
        youtube_user_info['customUrl'] = response_data['snippet']['customUrl']
    except:
        youtube_user_info['customUrl'] = ''
    youtube_user_info['publishedAt'] = response_data['snippet']['publishedAt']
    try:
        youtube_user_info['country'] = response_data['snippet']['country']
    except:
        youtube_user_info['country'] = ''
    youtube_user_info['viewCount'] = response_data['statistics']['viewCount']
    youtube_user_info['subscriberCount'] = response_data['statistics']['subscriberCount']
    youtube_user_info['videoCount'] = response_data['statistics']['videoCount']

if __name__ == '__main__':
    username = '顏毓麟KeennnyY'
    get_youtube_search(username)
    username = '刘亦菲'
    get_youtube_search(username)

