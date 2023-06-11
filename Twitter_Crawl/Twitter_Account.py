user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'

def tu_account_info(twitter_type):
    authorization = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    x_csrf_token = '8ee412e1e7867e4ee21f17d2f5b754b1778f6c320270fa75de168043978989688d61db2ee7d385d5b0899b1c1ef6be7bc75a9220fac99c0aaf70402767621d7642489c7e9697d2b1784bb71a804d5106'
    cookie = 'g_state={"i_l":0}; des_opt_in=Y; guest_id=v1%3A168148322805013385; kdt=SfMyQ213yF1nQm1Kc95Czsrh0RgJSmBD5si5EYtE; auth_token=19553facdad6f85df705aff197ac868612edf8c6; ct0=8ee412e1e7867e4ee21f17d2f5b754b1778f6c320270fa75de168043978989688d61db2ee7d385d5b0899b1c1ef6be7bc75a9220fac99c0aaf70402767621d7642489c7e9697d2b1784bb71a804d5106; twid=u%3D1596333572536692736; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A168148322805013385; guest_id_marketing=v1%3A168148322805013385; _ga=GA1.2.567330166.1682325914; personalization_id="v1_vC5VJ7d/sTQHArN85Djsdg=="; lang=en; _gid=GA1.2.1729726187.1683525924'
    UserByScreenName_id = 'sLVLhk0bGj3MVFEKTdax1w'
    UserTweets_id = 'CdG2Vuc1v6F5JyEngGpxVw'
    TweetDetail_id = 'BbCrSoXIR7z93lLCVFlQ2Q'
    Following_id = 'HExDl7BP0vveZdICk4d2ZA'

    twitter_header = {'user-agent':user_agent,'authorization':authorization,'x-csrf-token':x_csrf_token,'cookie':cookie}
    twitter_type_id = {'UserByScreenName':UserByScreenName_id,'UserTweets':UserTweets_id,'TweetDetail':TweetDetail_id,'Following':Following_id}
    if twitter_type == 'search':
        return twitter_header
    else:
        return twitter_header,twitter_type_id[twitter_type]

