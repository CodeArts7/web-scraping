import requests
# import json
# import csv
from datetime import datetime


def get_categories():
    headers = {
        'user-agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko)'
                      'Chrome / 107.0.0.0 Safari / 537.36',
        'accept': '*/*',
    }

    categories_lst = []
    sub_categories_lst = []
    super_categories_lst = []

    today_date = datetime.now().strftime('%d.%m.%Y')

    response = requests.get(url='https://supl.biz/api/monolith/rubrics/tree/ru/', headers=headers)

    # with open(f'info_{today_date}.json', 'w') as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)

    for number in range(28):
        category = response.json()[number].get('title')
        categories_lst.append(category)
        sub_cat = response.json()[number].get('children')
        for extra_number in range(70):
            try:
                sub_category = sub_cat[extra_number].get('title')
                sub_categories_lst.append(sub_category)
                super_cat = response.json()[number].get('children')[extra_number].get('children')
                for super_number in range(70):
                    try:
                        super_category = super_cat[super_number].get('title')
                        super_categories_lst.append(super_category)
                    except IndexError:
                        print(f'Сбор супер категорий из подкатегрии "{sub_category}" окончен.')
                        break
            except IndexError:
                print(f'Сбор из категории: "{category}" окончен.')
                break


def main():
    get_categories()


if __name__ == '__main__':
    main()