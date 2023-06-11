import json

import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 用于解决最大连接的问题
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def request_url_html(url,headers):
    response = session.get(url = url,headers = headers)
    response_data = etree.HTML(response.text)
    return response_data

def request_url_json(url,headers):
    response = session.get(url=url, headers = headers)
    print(response)
    try:
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data
    except:
        print(response.status_code,response)
        return None
