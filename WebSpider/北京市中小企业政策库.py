'''
#-*- codeing = utf-8 -*-
@Project    : OneSelfAll 
@File       : 北京市中小企业政策库.py
@Author     : TuTu
@CreateDate : 2023/7/5 15:05 
@UpdateDate : 2023/7/5 15:05 
'''
import base64
import chardet as chardet
import requests
import json
from lxml import etree

session = requests.session()
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

pageUrl = 'https://beijingtong.smebj.cn/apis/resource/manuscripts/get?token=618dff4cfaf4c1c9773701ad&data={}'
detailUrl = 'https://www.smebj.cn/detail/{}.html'

def getResponse(req_url):
    response = session.get(req_url,headers=header)
    # 解决中文乱码：获得网页编码，并将其设置为获取数据的编码
    encoding = chardet.detect(response.content)['encoding']
    response.encoding = encoding
    # type(responseText) : str
    responseText = response.text
    try:
        responseJson = json.loads(responseText)
        return responseText,responseJson
    except json.JSONDecodeError:
        responseTree = etree.HTML(responseText)
        return responseText,responseTree

def base64_encrypt(numPage):
    datadict = {
        "condition": {"state": "published", "whichpool": {"$in": ["ZC", "JD", "SB", "ZJ", "GS", "GG", "TZ", "ZQYJ"]},
                      "title": {"$regex": ""}}, "sort": {"publishtime": -1},
        "pagination": {"currentPage": numPage, "pageSize": 100}, "range": {"total": 1, "data": 1, "dicformat": "N"}}
    # 将Python字典转换为bytes类型
    data_bytes = json.dumps(datadict).encode('utf-8')
    # 使用base64进行编码
    encoded_data = base64.b64encode(data_bytes)
    # 将加密后的结果转换为字符串data
    base64_encode_str = encoded_data.decode('utf-8')
    return base64_encode_str

if __name__ == '__main__':
    # 23337，每页100条数据共234页
    writepath = '/mnt/public/data/Raw/beijingSmePolicy'
    with open(writepath,'w',encoding='utf-8') as wf:
        for i in range(1,235):
            page_url = pageUrl.format(base64_encrypt(235))
            responseJson = getResponse(page_url)[1]
            for item in responseJson['data']['list']:
                title = item['title']
                id = item['_id']
                author = item['author']
                artical_date = item['showenddate']
                detail_url = detailUrl.format(id)
                responseText = getResponse(detail_url)[0]
                newsitem = {
                    'id':id,
                    'title':title,
                    'artical_url':detail_url,
                    'author':author,
                    'artical_html':responseText,
                    'artical_date':artical_date,
                    'source':"北京市中小企业政策库"
                }
                wf.write(json.dumps(newsitem, ensure_ascii=False) + '\n')

