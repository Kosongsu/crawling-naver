import requests
from bs4 import BeautifulSoup

# BEST100 사이트 가져와서 html.parser p.ymd(년월일) 태그 찾아서 출력
NAVER_BEST100 = 'https://search.shopping.naver.com/best100v2/main.nhn'
shoppinglists = []
categories = ['인기검색', '패션의류', '패션잡화', '화장품/미용','디지털/가전', '가구/인테리어', '식품', '스포츠/레저', '출산/육아', '생활/건강']
source = requests.get(NAVER_BEST100).text
soup = BeautifulSoup(source, 'html.parser')
ymd = soup.select('p.ymd')

print(ymd[0].text.replace('.',''))

# TOP 10 상품명
popularbest10 = soup.find(id="popular_srch_lst")
popularbest10name = popularbest10.select(".txt")

for name in popularbest10name:
    print(name.text)
    shoppinglists.append(name.text)

# 카테고리 크롤
categorylists = soup.select("ul.type_normal")
for idx, category in enumerate(categorylists):
    for idx_2, item in enumerate(category.find_all('img')):
        name = item.get('alt')
        href = item.get('data-original')
        print(categories[idx], idx_2, name, href)