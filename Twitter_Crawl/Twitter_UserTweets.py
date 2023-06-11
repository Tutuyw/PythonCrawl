import json

from Common.common_request_url import request_url_json
from Twitter_Crawl.Twitter_Account import tu_account_info

def get_UserTweets(userId):
    global variable
    global features
    global twitter_header
    global UserTweets_id
    twitter_header = tu_account_info('UserTweets')[0]
    UserTweets_id = tu_account_info('UserTweets')[1]
    variable = {"userId": userId, "count": 10, "includePromotedContent": True, "withQuickPromoteEligibilityTweetFields":True, "withVoice":True, "withV2Timeline":True}
    features = {"blue_business_profile_image_shape_enabled":True,"responsive_web_graphql_exclude_directive_enabled":True,
                "verified_phone_label_enabled":False,"responsive_web_graphql_timeline_navigation_enabled":True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,"tweetypie_unmention_optimization_enabled":True,
                "vibe_api_enabled":True,"responsive_web_edit_tweet_api_enabled":True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,"view_counts_everywhere_api_enabled":True,
                "longform_notetweets_consumption_enabled":True,"tweet_awards_web_tipping_enabled":False,
                "freedom_of_speech_not_reach_fetch_enabled":True,"standardized_nudges_misinfo":True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":False,"interactive_text_enabled":True,
                "responsive_web_text_conversations_enabled":False,"longform_notetweets_rich_text_read_enabled":True,
                "responsive_web_enhance_cards_enabled":False}
    UserTweets_url = f'https://api.twitter.com/graphql/{UserTweets_id}/UserTweets?variables={json.dumps(variable)}&features={json.dumps(features)}'
    response_data = request_url_json(UserTweets_url, twitter_header)
    # return response_data
    UserTweets_list(response_data)

def UserTweets_list(response_data):
    instructions_list = response_data['data']['user']['result']['timeline_v2']['timeline']['instructions']
    for instruction in instructions_list:
        if instruction['type'] == 'TimelineAddEntries':
            tweets_list = instruction['entries']
            for tweet in tweets_list:
                print(tweet['entryId'])
                if 'homeConversation' in tweet['entryId']:
                    tweet_items = tweet['content']['items']
                    for item in tweet_items:
                        tweet_result = item['item']['itemContent']['tweet_results']['result']
                        Tweet_info(tweet_result)
                elif 'tweet' in tweet['entryId']:
                    tweet_result = tweet['content']['itemContent']['tweet_results']['result']
                    Tweet_info(tweet_result)
                elif 'cursor-bottom' in tweet['entryId']:
                    cursor_bottom_value = tweet['content']['value']
                    get_cursor_bottom(cursor_bottom_value)

def Tweet_info(tweet_result):
    tweetinfo = {}
    tweet_id = tweet_result['rest_id']
    user_domain = tweet_result['core']['user_results']['result']['legacy']['screen_name']
    tweetinfo['tweet_id'] = tweet_id
    tweetinfo['tweet_url'] = f'https://twitter.com/{user_domain}/status/{tweet_id}'
    tweetinfo['created_at'] = tweet_result['legacy']['created_at']
    tweetinfo['content_text'] = tweet_result['legacy']['full_text']
    content_picture = ''
    content_video = ''
    if 'extended_entities' in tweet_result['legacy'].keys():
        media = tweet_result['legacy']['extended_entities']['media'][0]
        if media['type'] == 'photo':
            content_picture = media['media_url_https']
        elif media['type'] == 'video':
            content_video = media['video_info']['variants'][1]['url']
    tweetinfo['content_picture'] = content_picture
    tweetinfo['content_video'] = content_video

    tweetinfo['reply_count'] = tweet_result['legacy']['reply_count']
    tweetinfo['retweet_count'] = tweet_result['legacy']['retweet_count']
    tweetinfo['quote_count'] = tweet_result['legacy']['quote_count']
    tweetinfo['favorite_count'] = tweet_result['legacy']['favorite_count']
    tweetinfo['bookmark_count'] = tweet_result['legacy']['bookmark_count']
    try:
        tweetinfo['veiws_count'] = tweet_result['views']['count']
    except:
        tweetinfo['veiws_count'] = ''

    tweetinfo['user_id'] = tweet_result['core']['user_results']['result']['rest_id']
    tweetinfo['user_domain'] = user_domain
    # tweetinfo['user_domain'] = tweet_result['core']['user_results']['result']['legacy']['screen_name']
    tweetinfo['user_screen_name'] = tweet_result['core']['user_results']['result']['legacy']['name']

    print(tweetinfo)

def get_cursor_bottom(cursor_bottom_value):
    print('下一页')
    variable['cursor'] = cursor_bottom_value
    UserTweets_url = f'https://api.twitter.com/graphql/{UserTweets_id}/UserTweets?variables={json.dumps(variable)}&features={json.dumps(features)}'
    response_data = request_url_json(UserTweets_url, twitter_header)
    UserTweets_list(response_data)

# get_UserTweets("1260553941714186241")
