import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

#https://hh.ru/search/vacancy?text=Python&from=suggest_post&fromSearchLine=true&area=1

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

url = 'https://hh.ru/search/vacancy'

vacancy_list = []

params = {
        'text': 'Python',
        'search_field': 'name',
        'page': 0,
        'hhtmFrom': 'vacancy_search_list'
    }

while True:
    session = requests.session()
    responce = session.get(url=url, params=params, headers=headers)
    dom = BeautifulSoup(responce.text, 'html.parser')
    vacancy = dom.find_all('div', {'class' : 'vacancy-serp-item__layout'})

