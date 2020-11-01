import time
from random import uniform
import urllib.request
import json
from powernad.API import RelKwdStat

client_id = "Vb7HEhsKJpmeY6RjbIzP"
client_secret = "iwDWmI7XEy"
NAVER_AD_CUSTOMER_ID = "2042427"
NAVER_AD_ACCESS_LICENSE = "01000000005372a15dfc223ec4f7e8372b9e1ffc5365139cd1572b39aba979b982403edf41"
NAVER_AD_SECRET_KEY = "AQAAAABTcqFd/CI+xPfoNyueH/xTcWu35E9aqdhVG/7uJGVrog=="

NAVER_AD_API_URL = "https://api.naver.com"
NAVER_BLOG_API_URL = "https://openapi.naver.com/v1/search/blog?query="
NAVER_SHOP_API_URL = "https://openapi.naver.com/v1/search/blog?query="

LIMIT = 30
keywords = []

def getSearchCount(keyword, URL):
    encText = urllib.parse.quote(keyword)
    url = URL + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    response_body = response.read()
    jsonString = response_body.decode('utf-8')
    jsonDict = json.loads(jsonString)
    if(rescode==200):
        totalCount = jsonDict['total']
    else:
        totalCount = 0   
    return totalCount
    
def naverRelKwdStat(keyword):
    relKwdStat = RelKwdStat.RelKwdStat(NAVER_AD_API_URL, NAVER_AD_ACCESS_LICENSE, NAVER_AD_SECRET_KEY, NAVER_AD_CUSTOMER_ID)
    kwDataList = relKwdStat.get_rel_kwd_stat_list(None, hintKeywords=keyword, showDetail='1')
    for idx, outdata in enumerate(kwDataList):
        time.sleep(uniform(0.3, 0.5)) 
        relKeyword = outdata.relKeyword 
        monthlyPcQcCnt = outdata.monthlyPcQcCnt 
        monthlyMobileQcCnt = outdata.monthlyMobileQcCnt
        monthlyAvePcCtr = outdata.monthlyAvePcCtr  
        monthlyAveMobileCtr = outdata.monthlyAveMobileCtr 
        compIdx = outdata.compIdx  
        blogsTotal = getSearchCount(relKeyword, NAVER_BLOG_API_URL)
        shopsTotal = getSearchCount(relKeyword, NAVER_SHOP_API_URL)                 

        if(str(monthlyPcQcCnt).isnumeric() and str(monthlyMobileQcCnt).isnumeric() and compIdx == "높음"):
            totalCnt = monthlyPcQcCnt + monthlyMobileQcCnt
            clickCnt = round(monthlyAvePcCtr + monthlyAveMobileCtr, 1)
            print(idx, relKeyword, totalCnt, clickCnt, blogsTotal, shopsTotal)
            keywords.append({ 'word': relKeyword, 'totalCnt': totalCnt, 'clickCnt': clickCnt, 'blogsTotal': blogsTotal, 'shopsTotal': shopsTotal })
            if(idx >= LIMIT):
                break

relKeyword = '마스크'
naverRelKwdStat(relKeyword)

