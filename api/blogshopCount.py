import urllib.request
import json

relKeyword = '마스크'

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
    items = jsonDict['items']

    for item in items:
        title = item['title']
        link = item['link']
        print('Title : ', title, ' Link : ', link)

    if(rescode==200):
        totalCount = jsonDict['total']
    else:
        totalCount = 0   
    return totalCount
    

blogsTotal = getSearchCount(relKeyword, NAVER_BLOG_API_URL)
shopsTotal = getSearchCount(relKeyword, NAVER_SHOP_API_URL)
print('Blog total : ', blogsTotal)
print('Shop total : ', shopsTotal)