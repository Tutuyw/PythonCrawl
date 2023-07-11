# 教育部学位与研究生教育发展中心：https://case.cdgdc.edu.cn/case/enterCaseCenter.do
import time

import requests
import json
from lxml import etree

s = requests.session()
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'cookie':'ajcwoLhKWU5gS=6059svPhZoKE2xYJZ4bOs2U7T2Fxxw8xrVX3fMm5Xsas5DUg2DGoyG6kmUcODbrblWDb_Ph0T1ohu_kCWlOPa4Jq; uniqueVisitorId=0eec792a-a442-b169-bfbd-157acc5191f6; Hm_lvt_417fbb550f24ced11fcc92c3a70afe67=1688377332,1688393532,1688437557; fileDownload=true; JSESSIONID=6A4155D1C03CE93865211134FCF497AB; Hm_lpvt_417fbb550f24ced11fcc92c3a70afe67=1688457974; ajcwoLhKWU5gT=0gQu1ib2uSNKvakx8sHrzri.5KhiNCDLUkyXMhPRIGcXqrANwfmA5YCuIaUPAihuhWl7QWPkMLeTYDcRN7GOXiq3a_6shFryUFbXeu8E8VrFJCn.rYGXSN3r39EcdBYvdRdTZ1p64mDvkengDKZapouH4GsEHoXlPN0zkmzGG40HLLeQnRRHJ0S0mbsq9Tq72mLSplCaVR0a2lG9p9O.3A52mcOl3HXagkKXAOUAUixb3S5P7tgpIf0jnToQ8YdWLtQbYJzOw_TAvTx2YerT3k5moE1PJZM4sDKmUMuiwjehTCwamxiiQdAZxT37Ix_0Bkz310chRurQGXmFBU0Nl_Bm3VR6Uj4_V7fso_PJlb4Z'
    # 'cookie':f'ajcwoLhKWU5gS=6059svPhZoKE2xYJZ4bOs2U7T2Fxxw8xrVX3fMm5Xsas5DUg2DGoyG6kmUcODbrblWDb_Ph0T1ohu_kCWlOPa4Jq; Hm_lvt_417fbb550f24ced11fcc92c3a70afe67={int(time.time())}; enable_ajcwoLhKWU5g=true; fileDownload=true; JSESSIONID=7A9C2BCFEE3A4A38E4C6776A7E1BDD5D; uniqueVisitorId=0eec792a-a442-b169-bfbd-157acc5191f6; Hm_lpvt_417fbb550f24ced11fcc92c3a70afe67=1688381936; ajcwoLhKWU5gT=06HlhOOGg89yFp12Z4ROMoLSoor05o6cmxFU.yW5mdnjPnT4lz7kCNYju3nTi4f5l1X6MpTH.9krkkHaOj8T0ILokINhDcFjlxiK2ouOeYIFRodV7eqWwHj4i4kwc3UK.sMdMotKQBxjHbw27XI8RQoMN4PbKwHPVhJXsPD6BKMhLx9Yky7BDMKiFfvri4BQcKBXbsHV1tRNv1HL2h5TCTNdCtUJ5byezTt4emENKdaHpeA3Oamh2_JGTCD979FbYmP5DqCEl6DcpSkuuKFxTIT2jmdSMmc8XOQ05mtJSJyWVofKJk3RxIA.YQdLf5f7kOZoOn.PNCNScqB1I_0ZFrkpKRvhI6.9FEls1gpzuhwE'

}
start_url = 'https://case.cdgdc.edu.cn/case/enterCaseCenter.do'

def get_categorys_list(start_url):
    response = s.get(start_url,headers=header)
    response_data = etree.HTML(response.text)
    categorys_list = response_data.xpath("//ul[@id='categorys']/li")
    print(categorys_list)

    for categorys in categorys_list:
        category_url = 'https://case.cdgdc.edu.cn/' + categorys.xpath("./div[@class='portlet_title']/a/@href")[0]
        category_name = categorys.xpath("./div[@class='portlet_title']/a/text()")[0]
        print(category_url,category_name)
        response = s.get(category_url, headers=header)
        print(response.text)

if __name__ == '__main__':
    # get_categorys_list(start_url)
    print(int(time.time()))
    test_url = 'https://case.cdgdc.edu.cn/member/case/operate/readContentDetail.do?caseId=63ed4c554591407691ba8227d82e47f4&fileId=bff539e0dd714d8c9958506486bde643'
    response = s.get(test_url, headers=header)
    # print(response.text)
    response_data = etree.HTML(response.text)
    # categorys_list = response_data.xpath("//ul[@id='categorys']/li")
    textLayer = response_data.xpath("//div[@class='textLayer']")
    print(response.text)