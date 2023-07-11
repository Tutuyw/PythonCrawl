'''
@Project : OneSelfAll 
@File    : 汉程国学宝典.py
@Author  : TuTu
@Date    : 2023/7/4 14:27 
'''
import chardet as chardet
import requests
import json
from lxml import etree

s = requests.session()
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}


if __name__ == '__main__':
    test_url = 'https://www.httpcn.com/'
    response = s.get(test_url, headers=header)
    # 解决中文乱码：获得网页编码，并将其设置为获取数据的编码
    encoding = chardet.detect(response.content)['encoding']
    response.encoding = encoding
    response_data = etree.HTML(response.text)
    menu = response_data.xpath("//ul[@class='life-nav-list clear']/li")
    for menu_item in menu:
        tag_url = 'https:' + menu_item.xpath("./a/@href")[0]
        tag_name = menu_item.xpath("./a/text()")[0]
        print(tag_url,tag_name)
    # print(menu)
