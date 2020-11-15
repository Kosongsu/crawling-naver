import urllib.request
import json

client_id = "Vb7HEhsKJpmeY6RjbIzP"
client_secret = "iwDWmI7XEy"

NAVER_BLOG_API_URL = "https://openapi.naver.com/v1/search/blog?query="
NAVER_SHOP_API_URL = "https://openapi.naver.com/v1/search/blog?query="

relKeyword = '치킨'

def getSearchCount(keyword, URL):
    encText = urllib.parse.quote(keyword)
    url = URL + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescod = response.getcode()
    response_body = response.read()
    jsonString = response_body.decode('utf-8')
    jsonDict = json.loads(jsonString)
    items = jsonDict['items']

