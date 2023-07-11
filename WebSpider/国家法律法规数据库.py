'''
#-*- codeing = utf-8 -*-
@File       : 国家法律法规数据库.py
@Author     : TuTu
@CreateDate : 2023/7/11 19:56 
@UpdateDate : 2023/7/11 19:56 
'''
import json
import time

from commonRequest import getResponse

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
"""
type
flfg：法律
xzfg：行政法规
jcfg：监察法规
sfjs：司法解释
dfxfg：地方性法规
"""

def getURL(typeKey):
    reqUrl = 'https://flk.npc.gov.cn/api/?'
    page = 1
    params = {
        'type': typeKey,
        'page': page,
        '_': int(time.time())
    }
    responseText, responseJson = getResponse('GET', reqUrl, header, params)
    data = responseJson['result']['data']
    while len(data):
        for item in data:
            policy = {
                'id':item['id'],
                'title':item['title'],
                'office':item['office'],
                'publishTime':item['publish'],
                'type':item['type'],
                'url':item['url']
            }
            yield  policy
        page += 1
        params['page'] = page
        params['_'] = int(time.time())
        print(params)
        responseText, responseJson = getResponse('GET', reqUrl, header, params)
        data = responseJson['result']['data']

if __name__ == '__main__':
    typeList = ['flfg','xzfg','jcfg','sfjs','dfxfg']
    writepath = ''
    with open(writepath,'w',encoding='utf-8') as wf:
        for typeKey in typeList:
            for policy in getURL(typeKey):
                print(policy)
                detailURL = 'https://flk.npc.gov.cn/api/detail'
                responseText, responseJson = getResponse('POST', detailURL, header,{'id':policy['id']})
                policy['pdfURL'] = ''
                policy['wordURL']= ''
                for pathitem in responseJson['result']['body']:
                    if pathitem['type'] in ['PDF']:
                        policy['pdfURL'] = 'https://wb.flk.npc.gov.cn{}'.format(pathitem['path'])
                    elif pathitem['type'] in ['WORD']:
                        policy['wordURL'] = 'https://wb.flk.npc.gov.cn{}'.format(pathitem['path'])
                if policy['pdfURL'] != '':
                    pathURL = policy['pdfURL']
                else:
                    pathURL = policy['wordURL']
                print('pathURL',pathURL)
                responseContent = getResponse('GET', pathURL, header)
                with open(f"{policy['title']}.{pathURL.split('.')[-1]}", 'wb') as wfp:
                    wfp.write(responseContent[0])

                wf.write(json.dumps(policy, ensure_ascii=False) + '\n')


