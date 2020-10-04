import urllib.request
import json

client_id = "Vb7HEhsKJpmeY6RjbIzP"
client_secret = "iwDWmI7XEy"

NAVER_BLOG_API_URL = "https://openapi.naver.com/v1/search/blog?query="
NAVER_SHOP_API_URL = "https://openapi.naver.com/v1/search/blog?query="

Keyword = '속옷'

def getSearchCount(Keyword, URL):
    encText = urllib.parse.quote(Keyword)
    url = URL + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    response_body = response.read()
    jsonString = response_body.decode('utf-8')
    jsonDict = json.loads(jsonString)
    items = jsonDict['items']

    for item in items:
        title = item['title']
        link = item['link']
        print('Title : ', title, 'link : ', link)

    if(rescode==200):
        totalCount = jsonDict['total']
    else:
        totalCount = 0
    return totalCount

blogsTotal = getSearchCount(Keyword, NAVER_BLOG_API_URL)
shopsTotal = getSearchCount(Keyword, NAVER_SHOP_API_URL)
print('Blog Total : ', blogsTotal)
print('Shop Total : ', shopsTotal)