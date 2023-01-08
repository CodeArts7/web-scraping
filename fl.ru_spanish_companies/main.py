import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.alimarket.es/empresas_directorio/area-logistica'
response = requests.get(url=url)
response.encoding='utf-8'
soup = BeautifulSoup(response.text, 'lxml')

companies_url = [f"https://www.alimarket.es/{a['href']}" for a in soup.find_all('a', href=True)][65:136]
companies_name = [a.text for a in soup.find_all('a', href=True)][65:136]

res = dict(zip(companies_name, companies_url))

with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(res, file, indent=4, ensure_ascii=False)
