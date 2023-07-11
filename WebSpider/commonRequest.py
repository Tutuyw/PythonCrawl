'''
#-*- codeing = utf-8 -*-
@File       : commonRequest.py
@Author     : TuTu
@CreateDate : 2023/7/10 15:18 
@UpdateDate : 2023/7/10 15:18 
'''
import requests
import json

import chardet as chardet
from lxml import etree
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 用于解决最大连接的问题
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def getResponse(method,req_url,header,dataparams=None):
    if method == 'GET':
        response = session.get(req_url,headers=header,params=dataparams)
    elif method == 'POST':
        response = session.post(req_url, headers=header,data=dataparams)
    # 解决中文乱码：获得网页编码，并将其设置为获取数据的编码
    encoding = chardet.detect(response.content)['encoding']
    # print('encoding',encoding)
    response.encoding = encoding
    # type(responseText) : str
    endstag = req_url.split('.')[-1]
    if endstag in ['pdf','docx']:
        responseContent = response.content
        return responseContent,None
    else:
        responseText = response.text
        try:
            # print(response.json())
            responseJson = json.loads(responseText)
            return responseText,responseJson
        except json.JSONDecodeError:
            responseTree = etree.HTML(responseText)
            return responseText,responseTree