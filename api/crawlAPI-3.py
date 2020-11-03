import flask
from flask_cors import CORS, cross_origin
import json
from functools import wraps
from flask import request, Response
import requests
from bs4 import BeautifulSoup
import urllib.request
from powernad.API import RelKwdStat
import time
from random import uniform

client_id = "Vb7HEhsKJpmeY6RjbIzP"
client_secret = "iwDWmI7XEy"
NAVER_AD_CUSTOMER_ID = "2042427"
NAVER_AD_ACCESS_LICENSE = "01000000005372a15dfc223ec4f7e8372b9e1ffc5365139cd1572b39aba979b982403edf41"
NAVER_AD_SECRET_KEY = "AQAAAABTcqFd/CI+xPfoNyueH/xTcWu35E9aqdhVG/7uJGVrog=="

NAVER_AD_API_URL = 'https://api.naver.com'
NAVER_BLOG_API_URL = 'https://openapi.naver.com/v1/search/blog?query='
NAVER_SHOP_API_URL = 'https://openapi.naver.com/v1/search/shop?query='

LIMIT = 0

app = flask.Flask(__name__)

# 리스트로 가져옴
def getSearchList(keyword, URL):
    searchList = []
    encText = urllib.parse.quote(keyword)
    url = URL + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    response_body = response.read()
    jsonString = response_body.decode('utf-8')
    jsonDict = json.loads(jsonString)
    items = jsonDict['items']
    for item in items:
        title = item['title']
        link = item['link']
        searchList.append({'title': title, 'link': link})
    print(searchList)
    return searchList

# blog, shop 개수
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

def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')

    return decorated_function

@app.route('/getPopularlists', methods=['GET'])
@as_json
def popularlist():
    NAVER_BEST100 = 'https://search.shopping.naver.com/best100v2/main.nhn#'
    popular10lists = []
    source = requests.get(NAVER_BEST100).text
    soup = BeautifulSoup(source, "html.parser")
    popular10 = soup.find(id="popular_srch_lst") 
    popular10names = popular10.select(".txt")

    for name in popular10names:
        popular10lists.append({"name": name.text})

    return popular10lists

@app.route('/relatedKeywords', methods=['GET'])
@as_json
def relatedKeywords():
    keywords = []
    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
    else:
        return "Error: keyword field"

    relKwdStat = RelKwdStat.RelKwdStat(NAVER_AD_API_URL, NAVER_AD_ACCESS_LICENSE, NAVER_AD_SECRET_KEY, NAVER_AD_CUSTOMER_ID)
    kwDataList = relKwdStat.get_rel_kwd_stat_list(None, hintKeywords=keyword, showDetail='1')
    for idx, outdata in enumerate(kwDataList):
        time.sleep(uniform(0.11, 0.12)) 
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

    return keywords

@app.route('/getBlogs', methods=['GET'])
@as_json
def getBlogs():
    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
    else:
        return "Error: keyword field"

    return getSearchList(keyword, NAVER_BLOG_API_URL)

@app.route('/getShops', methods=['GET'])
@as_json
def getShops():
    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
    else:
        return "Error: keyword field"

    return getSearchList(keyword, NAVER_SHOP_API_URL)

#app.run()
CORS(app)

# https://webisfree.com/2020-01-01/python-flask%EC%97%90%EC%84%9C-cors-cross-origin-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

if __name__ == '__main__':
    app.run()