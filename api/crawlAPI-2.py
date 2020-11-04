import flask
import json
from functools import wraps
from flask import request, Response
import requests
from bs4 import BeautifulSoup
import urllib.request
from powernad.API import RelKwdStat
import time
from random import uniform

LIMIT = 10

app = flask.Flask(__name__)

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
        return "Error: keyword field was not provided. Please enter a keyword."

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

app.run()