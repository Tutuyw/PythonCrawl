import json

import pymongo

from Common.common_request_url import request_url_json
from Twitter_Crawl.Twitter_Account import tu_account_info
from Twitter_Crawl.Twitter_UserByScreenName import User_info


def get_Following(userId):
    global variable, features, twitter_header, Following_id
    twitter_header = tu_account_info('Following')[0]
    Following_id = tu_account_info('Following')[1]

    variable = {"userId":userId,"includePromotedContent":False,'count':100}
    features = {"rweb_lists_timeline_redesign_enabled":False,"blue_business_profile_image_shape_enabled":True,"responsive_web_graphql_exclude_directive_enabled":True,"verified_phone_label_enabled":False,"creator_subscriptions_tweet_preview_api_enabled":False,"responsive_web_graphql_timeline_navigation_enabled":True,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,"tweetypie_unmention_optimization_enabled":True,"vibe_api_enabled":True,"responsive_web_edit_tweet_api_enabled":True,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,"view_counts_everywhere_api_enabled":True,"longform_notetweets_consumption_enabled":True,"tweet_awards_web_tipping_enabled":False,"freedom_of_speech_not_reach_fetch_enabled":True,"standardized_nudges_misinfo":True,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":False,"interactive_text_enabled":True,"responsive_web_text_conversations_enabled":False,"longform_notetweets_rich_text_read_enabled":True,"longform_notetweets_inline_media_enabled":False,"responsive_web_enhance_cards_enabled":False}
    Following_url = f'https://twitter.com/i/api/graphql/{Following_id}/Following?variables={json.dumps(variable)}&features={json.dumps(features)}'
    response_data = request_url_json(Following_url, twitter_header)
    UserFollowing_list(response_data)

def UserFollowing_list(response_data):
    print(response_data)
    instructions_list = response_data['data']['user']['result']['timeline']['timeline']['instructions']
    for instruction in instructions_list:
        if instruction['type'] == 'TimelineAddEntries':
            item_lists = instruction['entries']
            if len(item_lists) > 2:
                print('有用户')
                for item in item_lists:
                    print(item['entryId'])
                    if 'user' in item['entryId']:
                        try:
                            user_results = item['content']['itemContent']['user_results']['result']
                            Following_list.append(User_info(user_results))
                        except Exception as e:
                            print(e)
                            Following_list.append({'user_id':item['entryId']})
                    elif 'cursor-bottom' in item['entryId']:
                        cursor_bottom_value = item['content']['value']
                        get_cursor_bottom(cursor_bottom_value)
            else:
                print('没有下一页')



def get_cursor_bottom(cursor_bottom_value):
    print('下一页')
    variable['cursor'] = cursor_bottom_value
    Following_url = f'https://twitter.com/i/api/graphql/{Following_id}/Following?variables={json.dumps(variable)}&features={json.dumps(features)}'
    response_data = request_url_json(Following_url, twitter_header)
    UserFollowing_list(response_data)

conn = pymongo.MongoClient('mongodb://root:Bigdata#2021@175.27.160.162:27017/')
database = conn['ResourcePool']
collection_twitter_account = database['Account_Twitter']
for item in collection_twitter_account.find({'following_list':None,'source_event':None})[2:]:
    Following_list = []
    print(item['_id'])
    get_Following(item['_id'])
    collection_twitter_account.update_one({'_id':item['_id']},{'$set':{'following_list':Following_list}})

