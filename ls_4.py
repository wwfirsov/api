from lxml import html
import requests
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

url = 'https://yandex.ru/news/region/smolensk'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

news = []
items = dom.xpath("//div[contains(@class, 'mg-card_single')]")

for item in items[1:]:
    new = {}
    title = item.xpath(".//h2[@class='mg-card__title']/a/text()")
    link = item.xpath(".//h2[@class='mg-card__title']/a/@href")
    info = item.xpath(".//div[@class='mg-card__annotation']/text()")

    new['title'] = title
    new['link'] = link
    new['info'] = info

    news.append(new)


pprint(news)