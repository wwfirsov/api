from lxml import html
import requests
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=iphone&_sacat=0'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

phones = []
items = dom.xpath("//li[contains(@class,'s-item')]")
for item in items[1:]:
    phone = {}
    name = item.xpath(".//h3[@class='s-item__title']//text()")
    link = item.xpath(".//h3[@class='s-item__title']/../@href")
    price = item.xpath(".//span[@class='s-item__price']//text()")
    add_info = item.xpath(".//span[contains(@class,'s-item__hotness')]/span/text()")

    phone['name'] = name
    phone['link'] = link
    phone['price'] = price
    phone['add_info'] = add_info

    phones.append(phone)


pprint(phones)