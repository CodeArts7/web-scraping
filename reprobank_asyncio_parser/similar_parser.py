from bs4 import BeautifulSoup
import json
import time
import requests


result_json = []
parameters = ['Рост', 'Глаза', 'Волосы', 'Группа крови']
start_time = time.time()


def get_page_data():

    headers = {
        'user-agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) '
                      'Chrome / 108.0.0.0 Safari / 537.36',
        'accept': '*/*',
    }

    for page_number in range(1, 11):

        url = f'https://reprobank.ru/bank-donorov/katalog-donorov-spermi/?d_page={page_number}'
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        cards = soup.find('div', id='donors-catalog').find_all('div', class_='row')

        for card in cards:
            name = card.find('div', class_='link-detail')
            values = card.find_all('div', class_='value')
            result_json.append({
                'Донор': name.text.strip(),
                parameters[0]: values[0].text.strip(),
                parameters[1]: values[1].text.strip(),
                parameters[2]: values[2].text.strip(),
                parameters[3]: values[3].text.strip(),
            })

    with open('result_asyncio.json', 'w') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)


def main():
    get_page_data()

    finish_time = time.time() - start_time
    print(finish_time)


if __name__ == '__main__':
    main()
