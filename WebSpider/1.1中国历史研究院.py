'''
@Project : OneSelfAll 
@File    : 1.1 中国历史研究院.py
@Author  : TuTu
@Date    : 2023/7/4 17:02 
'''
import re
import chardet as chardet
import requests
import json
from lxml import etree

s = requests.session()
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
start_url = 'http://hrczh.cass.cn/sxqy/{}/'

def get_response(url):
    response = s.get(url, headers=header)
    # 解决中文乱码：获得网页编码，并将其设置为获取数据的编码
    encoding = chardet.detect(response.content)['encoding']
    response.encoding = encoding
    tree = etree.HTML(response.text)
    return tree,response.text

def get_next_page(tag_url,count_page):
    for index in range(1,count_page):
        url = f'{tag_url}index_{index}.shtml'
        responseTree = get_response(url)[0]
        yield url,responseTree

def getNewsItem(tree,tag_url):
    news_list = tree.xpath("//div[@class='news-fr fr newsList']/ul/li")
    for new in news_list:
        title = new.xpath(".//h4/a/text()")[0]
        artical_date = new.xpath(".//span[@class='year']/text()")[0] + new.xpath(".//span[@class='day']/text()")[0]
        artical_url = tag_url + new.xpath(".//h4/a/@href")[0][2:]
        artical_html = get_response(artical_url)[1]
        articalTree = get_response(artical_url)[0]
        try:
            Original_link = articalTree.xpath("//div[@class='TRS_Editor']//a/@href")[0]
            if Original_link[0] == '.':
                Original_link = tag_url + Original_link[2:]
        except:
            Original_link = ''
        print('原文链接',Original_link)
        p_text = articalTree.xpath("//div[@class='TRS_Editor']/p[last()-1]//text()")
        print(p_text)
        if p_text == ['......']:
            isFull = True
        else:
            isFull = False
        newsitem = {
            'title':title,
            'artical_url':artical_url,
            'artical_html':artical_html,
            'artical_date':artical_date,
            "Original_link": Original_link,
            "isFull": isFull,
            "source": "中国历史研究院",
        }
        yield newsitem

if __name__ == '__main__':
    with open('test.json','w',encoding='utf-8') as wf:
        tag_list = ['zl','kgx','zgs','sjs']
        for tag in tag_list:
            tag_url = start_url.format(tag)
            print(tag_url)
            responseTree = get_response(tag_url)[0]
            for newsitem in getNewsItem(responseTree,tag_url):
                print(newsitem)
                wf.write(json.dumps(newsitem,ensure_ascii=False)+'\n')

            page_div= responseTree.xpath("//div[@class='page-mod pchide']")[0]
            # 使用正则表达式匹配countPage的值
            match = re.search(r'var countPage = (\d+)', etree.tostring(page_div).decode())
            count_page = int(match.group(1))
            for nextUrl,nextTree in get_next_page(tag_url,count_page):
                print(nextUrl,nextTree)
                for newsitem in getNewsItem(nextTree, tag_url):
                    print(newsitem)
                    wf.write(json.dumps(newsitem, ensure_ascii=False) + '\n')


        tag_url = 'http://hrczh.cass.cn/lszg/lszg_wscl/'
        print(tag_url)
        responseTree = get_response(tag_url)[0]
        for newsitem in getNewsItem(responseTree, tag_url):
            print(newsitem)
            wf.write(json.dumps(newsitem, ensure_ascii=False) + '\n')

        page_div = responseTree.xpath("//div[@class='page-mod pchide']")[0]
        # 使用正则表达式匹配countPage的值
        match = re.search(r'var countPage = (\d+)', etree.tostring(page_div).decode())
        count_page = int(match.group(1))
        for nextUrl, nextTree in get_next_page(tag_url, count_page):
            print(nextUrl, nextTree)
            for newsitem in getNewsItem(nextTree, tag_url):
                print(newsitem)
                wf.write(json.dumps(newsitem, ensure_ascii=False) + '\n')

