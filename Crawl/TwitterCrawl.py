import json

from jsonsearch import JsonSearch

from Crawler.common_request_url import request_url_json
from Crawler.Twitter_URL import tu_account

class TwitterClass():
    def __init__(self):
        self.twitter_header = None
        self.request_url = None
        self.variable = None
        self.userentitylist = []
        self.tweetentitylist = []

    def getResponse(self,twitter_type,keyword):
        self.twitter_header = tu_account(twitter_type, keyword)[0]
        self.request_url = tu_account(twitter_type, keyword)[1]
        self.variable = tu_account(twitter_type, keyword)[2]
        response_data = request_url_json(self.request_url, self.twitter_header)
        return response_data

    def GetEntitylist(self,ResponseData):
        response_data = JsonSearch(object=ResponseData, mode='j')
        entries = response_data.search_all_value(key='entries')[0]
        if len(entries) > 2:
            for entry in entries:
                print(entry['entryId'])
                try:
                    # user表示用户信息
                    if 'user' in entry['entryId']:
                        user_result = entry['content']['itemContent']['user_results']['result']
                        userentityitem = self.TwitterUserInfo(user_result)
                        self.userentitylist.append(userentityitem)
                    # homeConversation表示该用户主页信息推文对话
                    elif 'homeConversation' in entry['entryId']:
                        tweet_items = entry['content']['items']
                        for item in tweet_items:
                            tweet_result = item['item']['itemContent']['tweet_results']['result']
                            tweetentityitem = self.TwitterTweetInfo(tweet_result)
                            self.tweetentitylist.append(tweetentityitem)
                    # tweet代表是该条博文的具体内容
                    elif 'tweet' in entry['entryId']:
                        tweet_result = entry['item']['itemContent']['tweet_results']['result']
                        tweetentityitem = self.TwitterTweetInfo(tweet_result)
                        self.tweetentitylist.append(tweetentityitem)
                    # conversationthread代表是该条博文的评论消息
                    elif 'conversationthread' in entry['entryId']:
                        conversationthread_items = entry['content']['items']
                        for conversationthread_item in conversationthread_items:
                            # tweet表示评论具体消息，cursor-showmore为显示更多按钮
                            if 'tweet' in conversationthread_item['entryId']:
                                tweet_result = conversationthread_item['item']['itemContent']['tweet_results']['result']
                                tweetentityitem = self.TwitterTweetInfo(tweet_result)
                                self.tweetentitylist.append(tweetentityitem)
                    elif 'cursor-bottom' in entry['entryId']:
                        try:
                            cursor_bottom_value = entry['content']['value']
                        except:
                            cursor_bottom_value = entry['content']['itemContent']['value']
                        nextResponse = self.GetCursorBottom(cursor_bottom_value)
                        self.GetEntitylist(nextResponse)
                except:
                    print(Exception)
            return self.userentitylist,self.tweetentitylist
        else:
            print('没有下一页')
            return False

    def GetCursorBottom(self,cursorvalue):
        print('下一页')
        self.variable['cursor'] = cursorvalue
        variables_start_index = self.request_url.index('variables=')
        features_start_index = self.request_url.index('&features=')
        next_cursor_url = f'{self.request_url[:variables_start_index]}variables={json.dumps(self.variable)}{self.request_url[features_start_index:]}'
        response_data = request_url_json(next_cursor_url, self.twitter_header)
        return response_data

    def TwitterUserInfo(self,result):
        useritem = {}
        useritem['domain'] = result['legacy']['screen_name']
        useritem['screen_name'] = result['legacy']['name']
        useritem['description'] = result['legacy']['description']
        useritem['created_at'] = result['legacy']['created_at']
        useritem['id'] = result['id']
        useritem['user_id'] = result['rest_id']
        try:
            useritem['location'] = result['legacy']['location']
        except:
            useritem['location'] = ""
        useritem['verified'] = result['legacy']['verified']
        useritem['profile_image_url_https'] = result['legacy']['profile_image_url_https']
        useritem['friends_count'] = result['legacy']['friends_count']
        useritem['followers_count'] = result['legacy']['followers_count']
        useritem['statuses_count'] = result['legacy']['statuses_count']
        useritem['media_count'] = result['legacy']['media_count']
        useritem['tweets_count'] = result['legacy']['listed_count']
        try:
            useritem['expanded_url'] = result['legacy']['url']
        except:
            useritem['expanded_url'] = ""
        return useritem

    def TwitterTweerInfo(self,result):
        tweetitem = {}
        tweet_id = result['rest_id']
        user_domain = result['core']['user_results']['result']['legacy']['screen_name']
        tweetitem['tweet_id'] = tweet_id
        tweetitem['tweet_url'] = f'https://twitter.com/{user_domain}/status/{tweet_id}'
        tweetitem['created_at'] = result['legacy']['created_at']
        tweetitem['content_text'] = result['legacy']['full_text']
        content_picture = ''
        content_video = ''
        if 'extended_entities' in result['legacy'].keys():
            media = result['legacy']['extended_entities']['media'][0]
            if media['type'] == 'photo':
                content_picture = media['media_url_https']
            elif media['type'] == 'video':
                content_video = media['video_info']['variants'][1]['url']
        tweetitem['content_picture'] = content_picture
        tweetitem['content_video'] = content_video

        tweetitem['reply_count'] = result['legacy']['reply_count']
        tweetitem['retweet_count'] = result['legacy']['retweet_count']
        tweetitem['quote_count'] = result['legacy']['quote_count']
        tweetitem['favorite_count'] = result['legacy']['favorite_count']
        tweetitem['bookmark_count'] = result['legacy']['bookmark_count']
        try:
            tweetitem['veiws_count'] = result['views']['count']
        except:
            tweetitem['veiws_count'] = ''

        tweetitem['user_id'] = result['core']['user_results']['result']['rest_id']
        tweetitem['user_domain'] = user_domain
        tweetitem['user_screen_name'] = result['core']['user_results']['result']['legacy']['name']
        return tweetitem



