from bs4 import BeautifulSoup
import requests
import json

categories = []
pagination = [89, 25, 20, 3, 86, 97, 7, 2, 6, 3, 1, 3, 3, 4]
result_json = []


def get_data():

    index_of_pagination = 0
    counter = 1

    url_f = 'https://samara.rusplitka.ru/'

    headers = {
        'user-agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 108.0.0.0 Safari / 537.36',
        'accept': '*/*'
    }

    response_f = requests.get(url=url_f, headers=headers)
    response_f.encoding='utf-8'
    soup_f = BeautifulSoup(response_f.text, 'lxml')

    urls = soup_f.find('ul', class_='list-unstyled').find_all('a', class_='btn btn-xs btn-default btn-block')

    for ur in urls:
        categories.append(ur['href'])

    for category in categories:
        for page in range(1, 2):
            url = f'https://samara.rusplitka.ru{category}page-{page}/'
            response = requests.get(url=url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')

            cards = soup.find_all('div', class_='item-body')

            for card in cards:
                try:
                    name = f"https://samara.rusplitka.ru{card.find('a', class_='title')['href']}"
                except:
                    name = 'Название не указано'

                try:
                    price = card.find('div', class_='price-block').find('span', itemprop='price').text.replace(' ', '')
                except:
                    price = 'Цена не указана'

                result_json.append({
                    'Cсылка на товар': f'{name}',
                    'Текущая цена': f'{price} руб.',
                })

        index_of_pagination += 1
        print(f'Категория №{counter} собрана!')
        counter += 1

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
