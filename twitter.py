'''
#-*- codeing = utf-8 -*-
@Project    : OneSelfAll 
@File       : twitter.py
@Author     : TuTu
@CreateDate : 2023/7/8 17:22 
@UpdateDate : 2023/7/8 17:22 
'''
import json

import requests

from jsonsearch import JsonSearch
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 用于解决最大连接的问题
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# TODO：需要更新自己的header
twitter_header = {
    'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-csrf-token':'c80b91ede981f484f4d5fe7b9ff33bb8ed9bae043462781e0fd3be77596b489eff6dd4b88d75b0f34c6d299217a0e7cf0dd139aa99d2327bb4a4b639797c2fb0176c3766865f530dedea24ffecd826fe',
    'cookie':'external_referer=padhuUp37zhD6%2F29CpQtyhGQCUl05AFo|0|8e8t2xd8A2w%3D; att=1-vxES9pVVmeeVmiIqn1VVebya61KCyBaMF3gdhMWj; _ga=GA1.2.218850823.1685936612; _gid=GA1.2.564776153.1685936612; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCKUip4mIAToMY3NyZl9p%250AZCIlMzJkZWFjODRhZDVhNDdmNmNmMDhkMDVlM2M1Y2NhOWM6B2lkIiU1M2Ew%250AZTg3ODYzMDA0ZDY0OTg5YTUwZThhNjQ1ZDhhZA%253D%253D--c94fe1be13b7cae1d2cf4cb00cd5ea8e8836aea0; guest_id=v1%3A168593661200605549; gt=1665609545614499840; g_state={"i_l":0}; kdt=OOo3L3fkO5Oi17U8VxPV8D2QHHGByoMsvVcFdZzD; auth_token=847a364abf3e6111f7a8df0dd01508e8988f331a; ct0=c80b91ede981f484f4d5fe7b9ff33bb8ed9bae043462781e0fd3be77596b489eff6dd4b88d75b0f34c6d299217a0e7cf0dd139aa99d2327bb4a4b639797c2fb0176c3766865f530dedea24ffecd826fe; lang=en; twid=u%3D1665609591756034048',
    'authorization':'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
}

def request_url_json(url, twitter_header):
    response = session.get(url=url, headers=twitter_header)
    # # print(response)
    # print(response.text)
    try:
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data
    except:
        print(response.status_code, response)

count = 0
def get_response(variables):
    global count
    count += 1
    # TODO：需要更新为自己的链接
    search_url = f'https://twitter.com/i/api/graphql/ukD99BOU37OlcBLMSDFRvQ/SearchTimeline?variables={json.dumps(variables)}&features=%7B%22rweb_lists_timeline_redesign_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
    print('第{}页'.format(count),variables)
    response_data = request_url_json(search_url, twitter_header)
    print(response_data)
    instructions = response_data['data']['search_by_raw_query']['search_timeline']['timeline']
    print(instructions)
    response_data = JsonSearch(object=response_data, mode='j')
    instructions = response_data.search_all_value(key='instructions')[0]
    for item in instructions:
        print(item)
    print(instructions)

variables = {"rawQuery": "(from:__Inty__) since:2022-01-01", "count": 20, "querySource": "typed_query", "product": "Latest"}
# variables = {"rawQuery": "(from:iingwen) until:2023-01-01 since:2022-01-01", "count": 20, "querySource": "typed_query", "product": "Latest"}
get_response(variables)