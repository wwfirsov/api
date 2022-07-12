from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import unicodedata
import json

text_to_url = 'python'

url = f'https://russia.superjob.ru/vacancy/search/'

session = requests.Session()
params = {'keywords': text_to_url, 'page': ''}
response = session.get(url, params=params)

res_html = BeautifulSoup(response.text, 'html.parser')

vac_name = res_html.find_all('span', class_='_2TI7V _21QHd _3SmWj')
vac_sal = res_html.find_all('span', class_='_4Gt5t f-test-text-company-item-salary')

names = [vac_name[i].text for i in range(len(vac_name))]
salary_min = [unicodedata.normalize("NFKD",vac_sal[i].text[-25:-10])[3:] if unicodedata.normalize("NFKD",vac_sal[i].text[-25:-10])[3:] != 'дого' else None for i in range(len(vac_sal))]
sal_val = [vac_sal[i].text[-10:-7] if vac_sal[i].text[-10:-7] != 'вор' else None for i in range(len(vac_sal))]
links = [url+vac_name[i].find('a').get('href') for i in range(len(vac_name))]

pages = res_html.find_all('span', class_='_28Wuq KNGBZ _4N0O3 _3lqNe _27m6C _R43B')
if len(pages):
    page_nums = int(pages[len(pages)-2].text)

    for i in range(2, page_nums):
        params = {'keywords': text_to_url, 'page': i}
        response = session.get(url, params=params)

        res_html = BeautifulSoup(response.text, 'html.parser')

        vac_name = res_html.find_all('span', class_='_2TI7V _21QHd _3SmWj')
        vac_sal = res_html.find_all('span', class_='_4Gt5t f-test-text-company-item-salary')

        names = names + [vac_name[i].text for i in range(len(vac_name))]
        salary_min = salary_min + [unicodedata.normalize("NFKD", vac_sal[i].text[-25:-10])[3:] if unicodedata.normalize("NFKD",vac_sal[i].text[-25:-10])[3:] != 'дого' else None for i in range(len(vac_sal))]
        sal_val = sal_val + [vac_sal[i].text[-10:-7] if vac_sal[i].text[-10:-7] != 'вор' else None for i in range(len(vac_sal))]
        links = links + [url + vac_name[i].find('a').get('href') for i in range(len(vac_name))]


sal_min = []
sal_max = []
for i in salary_min:
    if i:
        if i.find('—'):
            sal_min.append(i.split('—')[0].strip())
            if len(i.split('—')) > 1:
                sal_max.append(i.split('—')[1].strip())
            else:
                sal_max.append(None)
        else:
            sal_min.append(i)
            sal_max.append(None)
    else:
        sal_max.append(None)
        sal_min.append(None)

sal_min = [int(i.replace(' ','').strip()) if i else i for i in sal_min]
sal_max = [int(i.replace(' ','').strip()) if i else i for i in sal_max]


client = MongoClient('127.0.0.1', 27017)

mongo_db = client["salary_db"]
mongo_col = mongo_db["superjobs_vac"]

for i in range(len(names)):
    mong_data = mongo_col.find_one({'Название': names[i]})
    if not mong_data:
        x = mongo_col.insert_one({"Название": names[i],
                                  "Зарплата_мин": sal_min[i],
                                  "Зарплата_макс": sal_max[i],
                                  "Валюта": sal_val[i],
                                  "Ссылка": links[i]})
        print(f'id новой записи: {x.inserted_id}')

sal_to_find = 100000

sum_sal = {'$or': [{"Зарплата_мин":  {"$gt": int(f"{sal_to_find}")}}, {"Зарплата_макс": {"$gt": int(f"{sal_to_find}")}}]}
sum_sal_res = [i for i in mongo_col.find(sum_sal,{"_id" : 0, "Валюта" : 0,"Ссылка" : 0})]

json_string = json.dumps(sum_sal_res, indent=4, ensure_ascii=False)
print(f'Вакансии с зарплатой больше чем {sal_to_find}\n{json_string}')

count = 0

for x in mongo_col.find():
    count += 1

print(f'\nОбщее число записей в базе: {count}')


