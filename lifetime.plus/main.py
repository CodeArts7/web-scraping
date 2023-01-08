import requests
# import json
import csv
from datetime import datetime


def get_categories():
    headers = {
        'user-agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) '
                      'Chrome / 107.0.0.0 Safari / 537.36',
        'accept': 'application / json, text / plain, * / *',
    }

    res = []

    today_date = datetime.now().strftime('%d.%m.%Y')

    response = requests.get(url='https://www.lifetime.plus/api/analysis2', headers=headers)

    # with open(f'info_{today_date}.json', 'w') as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)

    categories = response.json()['categories']

    for category in categories:
        category_name = category['name']
        category_all_items = category['items']

        for category_item in category_all_items:
            item_name = category_item['name'].strip()
            item_price = category_item['price']
            item_description = category_item['description'].strip()
            item_day = category_item['days']
            item_bio = category_item['biomaterial']

            res.append([category_name, item_name, item_price, item_description, item_day, item_bio])

    with open(f'result_info_{today_date}', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Категория',
                'Анализ',
                'Стоимость',
                'Описание',
                'Готовность в днях',
                'Биоматериал',
            )
        )

        writer.writerows(res)


def main():
    get_categories()


if __name__ == '__main__':
    main()

