import json

from Common.common_request_url import request_url_json
from Twitter_Crawl.Twitter_Account import tu_account_info


def get_UserByScreenName(screen_name):
    twitter_header = tu_account_info('UserByScreenName')[0]
    UserByScreenName_id = tu_account_info('UserByScreenName')[1]
    variable = {"screen_name": screen_name, "withSafetyModeUserFields": True, "withSuperFollowsUserFields": True}
    features = {"blue_business_profile_image_shape_enabled":True,
                "responsive_web_graphql_exclude_directive_enabled": False, "verified_phone_label_enabled": False,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True}
    UserByScreenName_url = f'https://api.twitter.com/graphql/{UserByScreenName_id}/UserByScreenName?variables={json.dumps(variable)}&features={json.dumps(features)}'
    response_data = request_url_json(UserByScreenName_url, twitter_header)
    User_info(response_data)


def User_info(response_data):
    userinfo = {}
    try:
        result_data = response_data['data']['user']['result']
    except:
        result_data = response_data
    try:
        userinfo['id'] = result_data['id']
        userinfo['user_id'] = result_data['rest_id']
        userinfo['domain'] = result_data['legacy']['screen_name']
        userinfo['screenname'] = result_data['legacy']['name']
        userinfo['created_at'] = result_data['legacy']['created_at']
        try:
            userinfo['location'] = result_data['legacy']['location']
        except:
            userinfo['location'] = ''
        userinfo['description'] = result_data['legacy']['description']
        userinfo['profile_image_url'] = result_data['legacy']['profile_image_url_https']

        userinfo['followers_count'] = result_data['legacy']['followers_count']
        userinfo['friends_count'] = result_data['legacy']['friends_count']

        userinfo['statuses_count'] = result_data['legacy']['statuses_count']
        userinfo['listed_count'] = result_data['legacy']['listed_count']
        userinfo['media_count'] = result_data['legacy']['media_count']
        userinfo['favourites_count'] = result_data['legacy']['favourites_count']
    except:
        print('该用户暂时无法访问')
    print(userinfo)
    return userinfo

# get_UserByScreenName("whyyoutouzhele")

