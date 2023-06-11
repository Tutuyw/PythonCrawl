from facebook_scraper import get_posts, get_profile, get_group_info,get_posts_by_search
import requests
from http import cookiejar
import facebook_scraper as fb

file = "www.facebook.com_cookies.txt"
cookie = cookiejar.MozillaCookieJar()
cookie.load(file)
cookies = requests.utils.dict_from_cookiejar(cookie)
fb.set_cookies(cookies)
# for post in get_posts('jimmylindreamer', pages=1,options={'comments': True}):
#     print(post)
# POST_ID = 'pfbid0yN21p93mPKGmSTBdsip5j7wEqGjKM9Ymuo9v45eD8fMsKtuVoLLQ33uuPBuxu8zbl'
POST_ID = '1188321491831296'
# print(get_profile("jimmylindreamer",options={'friends':True}))

gen = get_posts(post_urls=[POST_ID])
post = next(gen)
print(post)
# for post in get_posts_by_search("林志颖"):
#     print(post)
print(get_profile("taiwanmemess"))