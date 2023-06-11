import time

from selenium import webdriver
from selenium.webdriver.common.by import By

path = '.\chromedriver.exe'
# https://www.youtube.com/@-luotianyi4050/videos
# https://www.youtube.com/@cnliziqi/videos
req_url = 'https://www.youtube.com/@cnliziqi/videos'
browser = webdriver.Chrome()    # (path):会出警告，但是可以用
browser.get(req_url)

pre_height = 0
now_height = 0

while True:
    browser.execute_script("scrollBy(0,10000)")  # 执行拖动滚动条操作
    time.sleep(1)
    now_height = browser.execute_script("return document.documentElement.scrollHeight;")
    if now_height == pre_height:  # 判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
        break
    pre_height = now_height
# js = "window.scrollTo(0, document.body.scrollHeight)"
# browser.execute_script(js) # 模拟鼠标滚轮，滑动页面至底部
video_lists = browser.find_elements(By.XPATH, "//div[@id='details']/div[@id='meta']")
videos_length = len(video_lists) - 1
print(videos_length)

for i in range(0,videos_length):
    href = video_lists[i].find_elements(By.XPATH, "./h3[@class='style-scope ytd-rich-grid-media']/a")[0].get_attribute('href')
    content = video_lists[i].find_elements(By.XPATH, "./h3[@class='style-scope ytd-rich-grid-media']/a")[0].get_attribute('aria-label')
    print(i, href, content)

browser.close()

