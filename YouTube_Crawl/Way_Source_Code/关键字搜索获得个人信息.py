import json
import re

import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def video_detail(video_id):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    response = requests.get(url=video_url, headers=headers)

    # 获得json数据
    json_text = re.findall('var ytInitialPlayerResponse = (.*?);var', response.text)[0]
    # print(json_str)
    json_data = json.loads(json_text)
    # print(json_data)
    # 视频链接(第一个) 音频链接（倒数第二个）还需要进行字符串截取
    # video_url = json_data['streamingData']['adaptiveFormats'][0]['signatureCipher']
    # audio_url = json_data['streamingData']['adaptiveFormats'][-2]['signatureCipher']

    # 视频详细信息：标题、作者、简介、时长、播放次数、发布时间
    title = json_data['videoDetails']['title']
    author = json_data['videoDetails']['author']
    shortDescription = json_data['videoDetails']['shortDescription']
    video_time = json_data['videoDetails']['lengthSeconds']
    viewCount = json_data['videoDetails']['viewCount']
    publishDate = json_data['microformat']['playerMicroformatRenderer']['publishDate']
    print(title, author, video_time, viewCount, publishDate)
    print(shortDescription)

def search_user_list(search_name):
    search_user_url = f'https://www.youtube.com/results?search_query={search_name}&sp=EgIQAg%253D%253D'
    response = requests.get(url=search_user_url, headers=headers)

    # 获得json数据
    json_text = re.findall('var ytInitialData = (.*?);</script>', response.text)[0]
    json_data = json.loads(json_text)
    response_data = json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

    for item in response_data:
        # 可能会出现广告,channelRenderer为搜索结果
        if 'channelRenderer' in item.keys():
            search_user = {}
            search_user['screen_name'] = item['channelRenderer']['title']['simpleText']
            search_user['domain'] = item['channelRenderer']['navigationEndpoint']['browseEndpoint']['canonicalBaseUrl']
            search_user['profile_image_url'] = 'https:' + item['channelRenderer']['thumbnail']['thumbnails'][0]['url']
            search_user['description'] = ''
            if 'descriptionSnippet' in item['channelRenderer'].keys():
                description_text = item['channelRenderer']['descriptionSnippet']['runs']
                for text_item in description_text:
                    search_user['description'] += text_item['text']
            search_user['followers_count'] = 0
            if 'videoCountText' in item['channelRenderer'].keys():
                search_user['followers_count'] = item['channelRenderer']['videoCountText']['simpleText']
            print(search_user)

def user_about_detail(user_name):
    user_about_url = f'https://www.youtube.com/@{user_name}/about'
    response = requests.get(url=user_about_url, headers=headers)

    # 获得json数据
    json_text = re.findall('var ytInitialData = (.*?);</script>', response.text)[0]
    json_data = json.loads(json_text)
    print(json_data)

    response_data = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs']
    print(response_data,len(response_data))
    for item in response_data:
        if 'tabRenderer' in item.keys():
            print(item['tabRenderer']['title'])
            # 简介、还差订阅数和视频数、外部链接
            if item['tabRenderer']['title'] in ['About','简介','簡介','關於']:
                item_content = item['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelAboutFullMetadataRenderer']
                user_about = {}
                user_about['screen_name'] = item_content['title']['simpleText']
                user_about['description'] = item_content['description']['simpleText']
                user_about['viewCountText'] = item_content['viewCountText']['simpleText']
                user_about['create_at'] = item_content['joinedDateText']['runs'][1]['text']
                user_about['country'] = ''
                if 'country' in item_content.keys():
                    user_about['country'] = item_content['country']['simpleText']
                print(user_about)
if __name__ =="__main__":
    video_id = 'mnMj285CTlU'
    # video_detail(video_id)

    search_keyword = '原神'
    # search_user_list(search_keyword)

    # Genshin_JP
    user_name = 'ruroroisme'
    user_about_detail(user_name)
    user_about_detail('Genshin_JP')



