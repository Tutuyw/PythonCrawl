import time

import pymongo
from lxml import etree

wiki_headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'cookie':'centralnotice_hide_WikiLovesFolklore2023International=%7B%22v%22%3A1%2C%22created%22%3A1677580557%2C%22reason%22%3A%22close%22%7D; centralnotice_hide_WikiLovesFolklore2023International=%7B%22v%22%3A1%2C%22created%22%3A1677580561%2C%22reason%22%3A%22close%22%7D; dismissASN=76036718; WMF-Last-Access=03-Mar-2023; WMF-Last-Access-Global=03-Mar-2023; GeoIP=US:CA:Los_Angeles:34.05:-118.24:v4; zhwikimwuser-sessionId=696ef53303902431713c; zhwikiwmE-sessionTickLastTickTime=1677814976357; zhwikiwmE-sessionTickTickCount=60'
}
# mongodb://bigdata2022:digital2022@172.17.33.225:27017/
# mongodb://root:Bigdata#2021@175.27.160.162:27017/
conn = pymongo.MongoClient('mongodb://root:Bigdata#2021@175.27.160.162:27017/')
database = conn['ResourcePool']

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_user_name():
    collection_read = database['entity']
    collection_save = database['wiki_entity_content']
    # "wiki_user_info.description":""
    # {'wiki_screen_name': '','wiki_url':{'$ne':""}}

    for item in collection_save.find({"type":"person","description":None})[1:]:

        wiki_name = item['wiki_name']
        print(wiki_name)
        response_data = get_response_page(wiki_name)
        description,resume,user_info = get_user_info(response_data)

        collection_save.update_one({'_id':item['_id']}, {'$set': {'description':description,'user_info': user_info,'resume':resume}})
        print(wiki_name,'更新成功')


def get_response_page(url):
    time.sleep(3)
    url = f'https://zh.wikipedia.org/wiki/{url}'  # 馬英九
    response = session.get(url=url, headers=wiki_headers)
    response_data = etree.HTML(response.text)
    return response_data

def get_user_info(response_data):
    # user_info = {}
    # 姓名与简介
    # name_path = response_data.xpath("//div[@id='mw-content-text']/div[@class='mw-parser-output']/table[@cellspacing='3'][1]/tbody/tr[1]//text()")
    # name = "".join(name_path)
    name = response_data.xpath("//h1[@id='firstHeading']/span[@class='mw-page-title-main']/text()")[0]
    # user_info['screen_name'] = name
    # description_path = response_data.xpath( "//p[preceding-sibling::table[@cellspacing='3'] and following-sibling::div[@id ='toc']]//text()")
    # description_path = response_data.xpath("//p[preceding-sibling::table[@role='presentation'] and following-sibling::div[@id ='toc']]//text()")
    description_path = response_data.xpath("//p[following-sibling::div[@id ='toc']]//text()")
    description = "".join(description_path)
    if description == '':
        description_path = response_data.xpath("//div[@id='mw-content-text']/div[@class='mw-parser-output']/p[following-sibling::h2[1]]//text()")
        description = "".join(description_path)
    # user_info['description'] = description

    table_tr_path = response_data.xpath("//div[@id='mw-content-text']/div[@class='mw-parser-output']/table[@cellspacing='3'][1]/tbody/tr[contains(/,th) and contains(/,td)]")
    count_num = response_data.xpath("count(//div[@id='mw-content-text']/div[@class='mw-parser-output']/table[@cellspacing='3'][1]/tbody/tr/th[contains(@style,'background:lavender;')])")
    test_xpath = "//div[@id='mw-content-text']/div[@class='mw-parser-output']/table[@cellspacing='3'][1]/tbody/tr/th[contains(@style,'background:lavender;')]/ancestor::tr"
    right_dict = []
    user_info = {}
    if count_num == 0.0:
        for item in table_tr_path:
            th_num = item.xpath("count(./th)")
            td_num = item.xpath("count(./td)")
            if th_num == td_num:
                th_name = item.xpath("./th[@scope='row']//text()")[0]
                td_value = item.xpath("./td//text()")
                td_value = "".join(td_value).replace("列表", "").replace("\n", " ").replace("\xa0", "")
                user_info.update({th_name: td_value})
    else:
        # 对符合条件的下标进行提取
        list_index = [0]
        for i in range(0,int(count_num)):
            test_two = response_data.xpath(f'{test_xpath}')[i]
            test_two_text = "".join(test_two.xpath(".//text()"))
            for item in table_tr_path[list_index[-1]:]:
                item_text = "".join(item.xpath(".//text()"))
                if item_text == test_two_text:
                    index = table_tr_path.index(item)
                    list_index.append(index)
                    break
        list_index.append(len(table_tr_path))
        print(list_index,list_index[-1])

        right_dict = {}
        for start,end in zip(list_index[1:-1],list_index[2:]):
            start_end = table_tr_path[start:end]
            print(start, end, len(start_end))
            tr_item_dict = get_tr_item(start_end)
            right_dict.update(tr_item_dict)
        print(right_dict)
        user_info = right_dict['个人资料']
        del right_dict['个人资料']
    return description,right_dict,user_info


def get_tr_item(start_end):
    tr_item_dict = {}
    tr_item_list = []
    th_td_dict = {}
    for item in start_end:

        th_num = item.xpath("count(./th)")
        td_num = item.xpath("count(./td)")

        if th_num == 1.0 and td_num==0.0 and ('background:lavender;' in item.xpath("./th/@style")[0]):
            th_colspan = "".join(item.xpath(".//text()")).replace("列表", "").replace("\n", " ").replace("\xa0","")

        if th_num == td_num:
            th_name = item.xpath("./th[@scope='row']//text()")[0]
            td_value = item.xpath("./td//text()")
            td_value = "".join(td_value).replace("列表","").replace("\n"," ").replace("\xa0","")
            th_td_dict.update({th_name:td_value})

        if th_num == 0.0 and td_num == 1.0:
            if item.xpath("count(./td/div/div)") != 0.0:
                th_value = item.xpath("./td/div/div//text()")[0]
                td_value = item.xpath("./td/div/ul//text()")
                td_value = "".join(td_value)
                th_td_dict.update({th_value:td_value})
            else:
                td_colspan = "".join(item.xpath(".//text()")).replace("列表", "").replace("\n", " ").replace("\xa0", "")
                if td_colspan != "" and td_colspan != " ":
                    tr_item_list.append(td_colspan)

        item_index = start_end.index(item)
        if item_index <= len(start_end)-2:
            next_th_num = start_end[item_index+1].xpath("count(./th)")
            next_td_num = start_end[item_index + 1].xpath("count(./td)")
            if next_th_num == 0.0 and next_td_num == 1.0:
                if th_td_dict != {}:
                    tr_item_list.append(th_td_dict)
                th_td_dict = {}

    if th_td_dict not in tr_item_list and th_td_dict != {}:
        tr_item_list.append(th_td_dict)
    tr_item_dict.update({th_colspan:tr_item_list})

    print(tr_item_dict)
    return tr_item_dict

def new_old_dict(new_dict,old_dict):
    ans_dict = {}
    for item in new_dict:
        if item not in old_dict:
            ans_dict.update({item:new_dict[item]})
    return ans_dict



if __name__ == "__main__":
    get_user_name()
    # search_name = '蔡英文'
    # response_data = get_response_page(search_name)
    # get_user_info(response_data)
    # get_response_page('廖天明')
    # get_response_page('国际妇女节')
    # user_info = get_user_info(response_data)
    # print(user_info)
    # # get_content()