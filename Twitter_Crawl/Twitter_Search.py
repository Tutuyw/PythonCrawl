import pymongo

from Common.common_request_url import request_url_json
from Twitter_Crawl.Twitter_Account import tu_account_info
from jsonsearch import JsonSearch

conn = pymongo.MongoClient('mongodb://root:Bigdata#2021@175.27.160.162:27017/')
database = conn['media_resp']
collection = database['litaiyuan']

def get_Search(query):
    global search_url, twitter_header
    twitter_header = tu_account_info('search')
    keyword_para = 'include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=false&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Cvibe'
    huati_para = 'include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=false&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&requestContext=launch&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Cvibe'
    # search_url = f'https://twitter.com/i/api/2/search/adaptive.json?q={query}&count=20&query_source=typed_query&{huati_para}'
    # (%23%E6%A2%A8%E6%B3%B0%E9%99%A2%E8%B8%A9%E8%B8%8F)%20until%3A2023-05-15%20since%3A2022-10-15
    search_url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=false&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=(%23%EC%A7%93%EB%B0%9F%EA%B8%B0)%20until%3A2023-05-15%20since%3A2022-10-15&query_source=typeahead_click&count=20&requestContext=launch&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Cvibe'
    response_data = request_url_json(search_url, twitter_header)
    get_tweet_info(response_data)

def get_tweet_info(response_data):
    print(response_data)
    tweets_items = response_data['globalObjects']['tweets']
    for tweet in tweets_items:
        tweet_info = {}
        tweet_info['_id'] = tweet
        tweet_info['created_at'] = tweets_items[tweet]['created_at']
        tweet_info['full_text'] = tweets_items[tweet]['full_text']
        tweet_info['reply_count'] = tweets_items[tweet]['reply_count']
        tweet_info['favorite_count'] = tweets_items[tweet]['favorite_count']
        tweet_info['retweet_count'] = tweets_items[tweet]['retweet_count']
        tweet_info['lang'] = tweets_items[tweet]['lang']
        tweet_info['user_id'] = tweets_items[tweet]['user_id_str']
        tweet_info['user_info'] = response_data['globalObjects']['users'][tweet_info['user_id']]
        tweet_info['response_data'] = tweets_items[tweet]
        try:
            collection.insert_one(tweet_info)
        except Exception as e:
            collection.update_one({'_id': tweet_info['_id']}, {'$set': tweet_info})
            print(e)
    if len(tweets_items) == 0:
        print('没有下一页')
    else:
        get_cursor_bottom(response_data)


def get_cursor_bottom(response_data):
    jsondata = JsonSearch(object=response_data, mode='j')
    cursor_list = jsondata.search_all_value(key='cursor')
    for cursor_item in cursor_list:
        if cursor_item['cursorType'] == 'Bottom':
            cursor_bottom = cursor_item['value']
        elif cursor_item['cursorType'] == 'Top':
            cursor_top = cursor_item['value']
    if cursor_bottom != cursor_top:
        cursor = cursor_bottom
        nextpage_url = f'{search_url}&cursor={cursor}'
        response_data = request_url_json(nextpage_url, twitter_header)
        get_tweet_info(response_data)
    else:
        print('没有下一页')

# 关键词搜索：梨泰院、梨泰院踩踏、Itaewon、이태원、Itaewon Stampede、짓밟기：-----"짓밟기" until:2023-05-15 since:2022-10-15
# 话题搜索：(#梨泰院) until:2023-05-15 since:2022-10-15
query = '(23이태원)%20until%3A2023-05-15%20since%3A2022-10-15'
get_Search(query)