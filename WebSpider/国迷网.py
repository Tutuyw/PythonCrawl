'''
@Project ：OneSelfAll 
@File    ：国迷网.py
@IDE     ：PyCharm 
@Author  ：TuTu
@Date    ：2023/7/3 22:02 
'''
import requests
import json
from lxml import etree

s = requests.session()
start_url = 'http://www.guoxuemi.com{}'

def get_html(keyword):
    url = start_url.format(keyword)
    response = s.get(url)
    try:
        if response.status_code == 200:
            response_data = etree.HTML(response.text)
            return response_data
    except:
        print(Exception)

def get_xgwz2_item(response_data):
    entry_title = response_data.xpath("//*[@class='entry-head']/h1/text()")[0]
    xgwz2_list = response_data.xpath("//*[@class='xgwz2']")
    print(xgwz2_list,len(xgwz2_list))
    result_list = []
    for item in xgwz2_list:
        item_href = item.xpath("./b/a/@href")[0]
        item_title = item.xpath("./b/a/text()")[0].replace('【','').replace('】','')
        item_title = entry_title+'_'+item_title
        print(item_title,item_href)
        result_list.append({item_title:item_href})
    return result_list

def get_class_list(keyword):
    response_data = get_html(keyword)
    shuku_list = get_xgwz2_item(response_data)
    result_url = []
    for item in shuku_list:
        (item_key,item_value), = item.items()
        response_data = get_html(item_value)
        item_list = get_xgwz2_item(response_data)
        result_url.append(item_list)
        print(item_list)
    return result_url

def get_li_item(item):
    (item_key,item_value), = item.items()
    response_data = get_html(item_value)
    li_list = response_data.xpath("//ul[@class='entry-related cols-3 post-loop post-loop-list']/li")
    result_list = []
    for item in li_list:
        item_title = item.xpath("./a/text()")[0]
        item_href = item.xpath("./a/@href")[0]
        item_title = item_key + '_' + item_title
        result_list.append({item_title:item_href})
        print({item_title:item_href})
    return result_list

def get_title_list(class_list):
    article_list = []
    for item_list in class_list:
        for item_class in item_list:
            print(item_class)
            temp_list = get_li_item(item_class)
            for item in temp_list:
                article_list = article_list + get_li_item(item)
    return article_list

def save(article_list):
    with open('/mnt/user/tuyuwei/raw_data/guoxuemi.json','a',encoding='utf-8') as writefile:
        for item in article_list:
            (item_key,item_value), = item.items()
            line = {
                'title':item_key,
                'url':start_url.format(item_value),
                'original_html':s.get(start_url.format(item_value)).text
            }
            writefile.write(json.dumps(line,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    keyword = '/shuku/'
    class_list = get_class_list(keyword)
    article_list = get_title_list(class_list)
    save(article_list)

    print(len(article_list),article_list[-1])

