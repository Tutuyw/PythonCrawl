'''
#-*- codeing = utf-8 -*-
@Project    : OneSelfAll 
@File       : 国家哲学社会科学学术期刊数据库.py
@Author     : TuTu
@CreateDate : 2023/7/10 15:17 
@UpdateDate : 2023/7/10 15:17
'''
import json
import os

'''
1、在getJournalnavigation()获得期刊的列表及gch
2、在getYearList(gch)获得期刊的所有年份
3、在getYearList(gch,yearNum)获得期刊某一年份的期号列表
4、根据某一期号获得某一期号的所有文章的id
5、根据文章id获得某一文章的路径
6、根据文章路径下载文章的pdf
'''
import datetime
import hashlib

from commonRequest import getResponse

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

def getJournalnavigation(start,end):
    JournallistURl = 'https://www.nssd.cn/web/journalnavigation/journalGuide/list.do'
    params = {
        'pageSize': 5,
        'orderType': 'firstPName',
        'selectType': 'subclass',
        'searchLink': 'https://www.nssd.cn/html/1/155/index.html'
    }
    for page in range(start,end+1):
        params['pageNo'] = page
        responseText, responseJson = getResponse('POST', JournallistURl, header, params)
        rows = responseJson['data']['rows']
        for row in rows:
            rowitem = {}
            rowitem['periodname'] = row['periodname']
            rowitem['gch'] = row['gch']
            rowitem['briefintroduction'] = row['briefintroduction']
            rowitem['firstclass'] = row['firstclass']
            yield rowitem

def getYearList(gch,firstclass):
    # req_url = 'https://www.nssd.cn/web/journalnavigation/zwqkinfo/get.do?gch={}&yearNum=&type=0&isLU=true&userId=763587'
    # 获得年份列表
    catalog1Url = 'https://www.nssd.cn/web/journalnavigation/zwqkinfo/catalog1.do?gch={}&yearNum={}&isLU=true&firstclass={}'
    # 获得每年期号列表
    catalogUrl = 'https://www.nssd.cn/web/journalnavigation/zwqkinfo/catalog.do?gch={}&yearNum={}&isLU=true&firstclass={}'
    responseText, responseJson = getResponse('GET', catalog1Url.format(gch,'',firstclass), header)
    for yearitem in responseJson['data']['yearList']:
        yearNum = yearitem['href'].split('/')[4]
        print('yearNum',yearNum)
        responseText, responseJson = getResponse('GET', catalog1Url.format(gch,yearNum,firstclass), header)
        for numitem in responseJson['data']['numList']:
            numNum = numitem['href'].split('/')[4]
            numText = numitem['text']
            print('numNum', numNum,numText)
            responseText, responseJson = getResponse('GET', catalogUrl.format(gch,numNum,firstclass), header)
            for articleList in responseJson['data']['articleList']:
                for article in articleList['articleList']:
                    articleId = article['id']
                    title = article['text']
                    yield articleId,title,numText

def downPDF(articleId,filepath):
    downLoadURL = 'https://www.nssd.cn/web/paper/downLoad.do'
    onlineURL = 'https://www.nssd.cn/web/paper/online.do'
    params = {
        'userId': 763587,
        'suid': articleId,
    }
    responseText, responseJson = getResponse('POST', onlineURL, header, params)
    path = responseJson['data']['path']
    pdfUrl = 'https://ft.ncpssd.org/pdf/getn/{}'.format(path)
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    # Generate the sign
    key = 'L!N45S26y1SGzq9^'
    sign = hashlib.md5((key + current_date).encode()).hexdigest()
    # print(pdfUrl)
    pdfheader = {
        'sign':sign,
        'userInfo':'763587',
        'site':'nssd',
        'dotype':'down',
    }
    responseContent = getResponse('GET',pdfUrl,pdfheader)
    with open(f'{filepath}.pdf','wb') as wf:
        wf.write(responseContent[0])

def getDetail(id):
    detailURL = 'https://www.nssd.cn/web/paper/findById.do?lngId={}'
    responseText, responseJson = getResponse('GET', detailURL.format(id), header)
    paper = {}
    paper['id'] = id
    paper['journalName'] = responseJson['data'].get('mediaid', '')
    paper['title'] = responseJson['data'].get('title_c', '')
    paper['author'] = responseJson['data'].get('writer', '')
    paper['keyword'] = responseJson['data'].get('keyword_py', '')
    paper['publishdate'] = responseJson['data'].get('publishdate', '')
    paper['organ'] = responseJson['data'].get('organ', '')
    paper['journalqk'] = responseJson['data'].get('medias_qk', '')
    paper['summary'] = responseJson['data'].get('remark_c', '')
    paper['class'] = responseJson['data'].get('classids_g1', [])
    paper['url'] = detailURL.format(id)
    return paper



if __name__ == '__main__':
    # getJournalnavigation(1,116)
    for row in getJournalnavigation(1,1):
        for id,title,numText in getYearList(row['gch'],row['firstclass']):
            print(id,title)
            folder_path = f"./{row['periodname']}/{numText}/"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # downPDF(id,f'{folder_path}/{title}')
            paper = getDetail(id)
            with open(f"./{row['periodname']}/{row['periodname']}.json",'a',encoding='utf-8') as wf:
                print(paper)
                wf.write(json.dumps(paper,ensure_ascii=False)+'\n')


