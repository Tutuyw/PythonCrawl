import json

from Common.common_request_url import request_url_json
from Twitter_Crawl.Twitter_Account import tu_account_info
from Twitter_Crawl.Twitter_UserTweets import Tweet_info


def get_TweetDetail(TweetId):
    global variable, features, twitter_header, TweetDetail_id
    twitter_header = tu_account_info('TweetDetail')[0]
    TweetDetail_id = tu_account_info('TweetDetail')[1]
    variable = {"focalTweetId":TweetId,"with_rux_injections":False,"includePromotedContent":True,"withCommunity":True,"withQuickPromoteEligibilityTweetFields":True,"withBirdwatchNotes":True,"withVoice":True,"withV2Timeline":True}
    features = {"blue_business_profile_image_shape_enabled":True,"responsive_web_graphql_exclude_directive_enabled":True,"verified_phone_label_enabled":False,"responsive_web_graphql_timeline_navigation_enabled":True,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,"tweetypie_unmention_optimization_enabled":True,"vibe_api_enabled":True,"responsive_web_edit_tweet_api_enabled":True,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,"view_counts_everywhere_api_enabled":True,"longform_notetweets_consumption_enabled":True,"tweet_awards_web_tipping_enabled":False,"freedom_of_speech_not_reach_fetch_enabled":True,"standardized_nudges_misinfo":True,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":False,"interactive_text_enabled":True,"responsive_web_text_conversations_enabled":False,"longform_notetweets_rich_text_read_enabled":True,"responsive_web_enhance_cards_enabled":False}
    TweetDetail_url = f'https://api.twitter.com/graphql/{TweetDetail_id}/TweetDetail?variables={json.dumps(variable)}&features={json.dumps(features)}'
    response_data = request_url_json(TweetDetail_url, twitter_header)
    TweetDetail(response_data)

def TweetDetail(response_data):
    instructions = response_data['data']['threaded_conversation_with_injections_v2']['instructions']
    for instruction in instructions:
        if instruction['type'] == 'TimelineAddEntries':
            TimelineAddEntries_entries = instruction['entries']
            for TimelineAddEntries_entry in TimelineAddEntries_entries:
                # tweet代表是该条博文的具体内容
                if 'tweet' in TimelineAddEntries_entry['entryId']:
                    tweet_result = TimelineAddEntries_entry['content']['itemContent']['tweet_results']['result']
                    Tweet_info(tweet_result)
                # conversationthread代表是该条博文的评论消息
                elif 'conversationthread' in TimelineAddEntries_entry['entryId']:
                    conversationthread_items = TimelineAddEntries_entry['content']['items']
                    for conversationthread_item in conversationthread_items:
                        # tweet表示评论具体消息，cursor-showmore为显示更多按钮
                        if 'tweet' in conversationthread_item['entryId']:
                            tweet_result = conversationthread_item['item']['itemContent']['tweet_results']['result']
                            Tweet_info(tweet_result)
                # 翻页
                elif 'cursor-bottom' in TimelineAddEntries_entry['entryId']:
                    cursor_bottom_value = TimelineAddEntries_entry['content']['itemContent']['value']
                    get_TweetDetail_cursor_bottom(cursor_bottom_value)

def get_TweetDetail_cursor_bottom(cursor_bottom_value):
    print('下一页')
    variable['cursor'] = cursor_bottom_value
    TweetDetail_url = f'https://api.twitter.com/graphql/{TweetDetail_id}/TweetDetail?variables={json.dumps(variable)}&features={json.dumps(features)}'
    response_data = request_url_json(TweetDetail_url, twitter_header)
    TweetDetail(response_data)

# get_TweetDetail('1653396001145729024')



