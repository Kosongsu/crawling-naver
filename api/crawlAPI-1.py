import flask
import json
from functools import wraps
from flask import request, Response
import requests
from bs4 import BeautifulSoup

app = flask.Flask(__name__)

# json 형식 변환
def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')

    return decorated_function

# 크롤링 웹서비스 올리기 인기상품 10개
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

app.run()