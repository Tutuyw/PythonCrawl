"""
create_time:2023/01/12
update_time:2023/01/30

基本功能：获得一级评论以及二级评论的相关信息：评论用户、评论时间、评论内容、评论获赞数
改进点：
【已完成】 1、如果回复数超过10条，需要点击“显示更多回复”
2、如果二级回复的评论者是发布视频的人的话，需要重新写xpath解析获得评论者名称
3、将视频的相关信息添加
4、添加字段用于存储表情（问题，YouTube是否可以图片评论）
5、其他健壮性问题
"""
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

path = './chromedriver.exe'
# https://www.youtube.com/watch?v=wgnCtdudFzg
# https://www.youtube.com/watch?v=u-xS-dkz3a0
# https://www.youtube.com/watch?v=wdi2SRcZaVE
# https://www.youtube.com/watch?v=48OtHl0C2Bo
# 1、https://www.youtube.com/watch?v=thdCksamSog&t=3s 戏中人间——《原神》云堇创作的幕后
# 2、https://www.youtube.com/watch?v=EiAhMr6IJTQ 《原神》剧情PV-「神女劈观」
# 3、https://www.youtube.com/watch?v=YxIa114Od84  《原神》角色演示-「云堇：虹章书真意」
# 4、https://www.youtube.com/watch?v=UJ7NrBAKtAA  《原神》拾枝杂谈-「云堇：妙曲压台」
# 5、https://www.youtube.com/watch?v=nzWmXzoYiSI  Genshin Chinese VA - The Divine Damsel of Devastation [神女劈观] Yunjin云堇 (Lyrics Chi/Pin/Eng)
# 6、https://www.youtube.com/watch?v=O8bzUg0yLps The Divine Damsel of Devastation Opera Performance but it's IRL
# 7、https://www.youtube.com/watch?v=KbB4YS8xFjI  Devastation and Redemption ("Fleeting Colors in Flight" Original Game Soundtrack EP)
req_url = 'https://www.youtube.com/watch?v=YxIa114Od84 '
browser = webdriver.Chrome()  # (path):会出警告，但是可以用
browser.get(req_url)
wait = WebDriverWait(browser, 30)

browser.execute_script("scrollBy(0,500)")
time.sleep(5)
# 获取排序方式按钮并点击
order_btn = browser.find_elements(By.XPATH, "//yt-icon[@id='label-icon']")  #div[@id='icon-label']
time.sleep(1)
order_btn[0].click()
time.sleep(2)
# # 按时间排序
# time_comment_btn = browser.find_element(By.XPATH,
#                                         "//a[@class='yt-simple-endpoint style-scope "
#                                         "yt-dropdown-menu']/tp-yt-paper-item/tp-yt-paper-item-body/div[@class='item style-scope "
#                                         "yt-dropdown-menu']")
# time_comment_btn.click()
# time.sleep(1)
# 按热度排序
hot_comment_btn = browser.find_element(By.XPATH,"//a[@class='yt-simple-endpoint style-scope yt-dropdown-menu iron-selected']/tp-yt-paper-item/tp-yt-paper-item-body/div[@class='item style-scope "
                                        "yt-dropdown-menu']")
hot_comment_btn.click()
time.sleep(1)

pre_height = 0
now_height = 0
temp_height = 0
re_num = 0

while True:
    browser.execute_script("scrollBy(0,10000)")  # 执行拖动滚动条操作
    time.sleep(10)
    # 方法一：判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
    now_height = browser.execute_script("return document.documentElement.scrollHeight;")
    print(pre_height, now_height)
    if now_height == pre_height:
        break
    pre_height = now_height

    # # 方法二：判断当前滚动条距离顶部的距离，若和上一次相等说明到底了
    # check_height = browser.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
    # if check_height == temp_height:
    #     break
    # temp_height = check_height
    # print(check_height)


# 判断是否有回复。有则点击展开回复按钮获取
# 方法2：
time.sleep(10)
expander_btns = browser.find_elements(By.XPATH,"//ytd-button-renderer[@id='more-replies']/yt-button-shape/button")
print(len(expander_btns))
for expander_btn in expander_btns:
    comment_replies_content = expander_btn.find_element(By.XPATH,"./div/span").text
    element = expander_btn.find_element(By.XPATH,"./yt-touch-feedback-shape/div/div[2]")
    time.sleep(5)
    # 跳转到对应位置
    browser.execute_script("arguments[0].scrollIntoView();", element)
    # 点击展开回复列表
    browser.execute_script("arguments[0].click();", element)
    re_num = re_num + 1
    print(re_num, comment_replies_content)
while True:
    more_btns = browser.find_elements(By.XPATH,"//div[@id='button']/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
    print(len(more_btns))
    # 如果”显示更多回复“的按钮长度为0代表都已经展开了
    if len(more_btns) == 0:
        break
    for more_btn in more_btns:
        # 跳转到对应位置
        browser.execute_script("arguments[0].scrollIntoView();", more_btn)
        # 点击展开显示更多回复
        browser.execute_script("arguments[0].click();", more_btn)
    time.sleep(5)

time.sleep(10)
comment_lists = browser.find_elements(By.XPATH, "//div[@id='contents']/ytd-comment-thread-renderer")
comment_length = len(comment_lists)
print(comment_length)
comment_mes_list = []
for i in range(0,comment_length):
    comment_mes = {}
    # 获得一级评论
    comment_mes['index'] = i
    comment_author = comment_lists[i].find_elements(By.XPATH,"./ytd-comment-renderer/div[@id='body']/div[@id='main']/div[@id='header']/div[@id='header-author']/h3/a")[0].text
    comment_time = comment_lists[i].find_elements(By.XPATH,"./ytd-comment-renderer/div[@id='body']/div[@id='main']/div[@id='header']/div[@id='header-author']/yt-formatted-string/a")[0].text
    comment_content = comment_lists[i].find_elements(By.XPATH,"./ytd-comment-renderer/div[@id='body']/div[@id='main']/div[@id='comment-content']/ytd-expander/div/yt-formatted-string")[0].text
    comment_content = comment_content.replace('','').replace('\n','')
    comment_like_num = comment_lists[i].find_elements(By.XPATH,"./ytd-comment-renderer/div[@id='body']/div[@id='main']/ytd-comment-action-buttons-renderer/div[@id='toolbar']/span[@id='vote-count-middle']")[0].text
    comment_mes['author'] = comment_author
    comment_mes['time'] = comment_time
    comment_mes['content'] = comment_content
    print(comment_mes)
    comment_mes_list.append(comment_mes)

    # 获取二级评论，即评论的回复
    comment_replies_list = comment_lists[i].find_elements(By.XPATH, "./div[@id='replies']/ytd-comment-replies-renderer/div[@id='expander']/div[@id='expander-contents']/div[@id='contents']/ytd-comment-renderer")
    if len(comment_replies_list) != 0:
        print(comment_author,len(comment_replies_list))
        for replies in comment_replies_list:
            replies_mes = {}
            replies_mes['index'] = '-'
            replies_author = replies.find_elements(By.XPATH,"./div[@id='body']/div[@id='main']/div[@id='header']/div[@id='header-author']/h3/a/span")[0].text
            replies_time = replies.find_elements(By.XPATH,"./div[@id='body']/div[@id='main']/div[@id='header']/div[@id='header-author']/yt-formatted-string/a")[0].text
            a_num = replies.find_elements(By.XPATH,"./div[@id='body']/div[@id='main']/div[@id='comment-content']/ytd-expander/div/yt-formatted-string/a")
            # print(len(a_num))
            if len(a_num) == 0:
                replies_content = replies.find_elements(By.XPATH,"./div[@id='body']/div[@id='main']/div[@id='comment-content']/ytd-expander/div/yt-formatted-string")[0].text
            else:
                replies_content = replies.find_elements(By.XPATH,"./div[@id='body']/div[@id='main']/div[@id='comment-content']/ytd-expander/div/yt-formatted-string/span")[0].text
            replies_content = replies_content.replace('\n', '')
            replies_like_num = replies.find_elements(By.XPATH, "./div[@id='body']/div[@id='main']/ytd-comment-action-buttons-renderer/div[@id='toolbar']/span[@id='vote-count-middle']")[0].text
            replies_mes['author'] = replies_author
            replies_mes['time'] = replies_time
            replies_mes['content'] = replies_content
            print(replies_mes)
            comment_mes_list.append(replies_mes)

header_filed = ['index', 'author', 'time','content']
with open('视频3.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=header_filed)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
    writer.writeheader()  # 写入列名
    writer.writerows(comment_mes_list)  # 写入数据
print("数据已经全部写入成功！！！")

# browser.close()
# if __name__ == "__main__":
#
#     pass