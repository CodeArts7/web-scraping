import requests
from bs4 import BeautifulSoup
import time
import json


start_time = time.time()


def get_data():

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'accept': '*/*',
    }

    categories = ['development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other&',
                  'testing_sites%2Ctesting_mobile%2Ctesting_software&',
                  'admin_servers%2Cadmin_network%2Cadmin_databases%2Cadmin_security%2Cadmin_other&',
                  'design_sites%2Cdesign_landings%2Cdesign_logos%2Cdesign_illustrations%2Cdesign_mobile%2Cdesign_icons%2Cdesign_polygraphy%2Cdesign_banners%2Cdesign_graphics%2Cdesign_corporate_identity%2Cdesign_presentations%2Cdesign_modeling%2Cdesign_animation%2Cdesign_photo%2Cdesign_other&',
                  'content_copywriting%2Ccontent_rewriting%2Ccontent_audio%2Ccontent_article%2Ccontent_scenarios%2Ccontent_naming%2Ccontent_correction%2Ccontent_translations%2Ccontent_coursework%2Ccontent_specification%2Ccontent_management%2Ccontent_other&',
                  'marketing_smm%2Cmarketing_seo%2Cmarketing_context%2Cmarketing_email%2Cmarketing_research%2Cmarketing_sales%2Cmarketing_pr%2Cmarketing_other&',
                  'other_audit_analytics%2Cother_consulting%2Cother_jurisprudence%2Cother_accounting%2Cother_audio%2Cother_video%2Cother_engineering%2Cother_other&',
                  ]

    categories_for_json = ['Разработка', 'Тестирование', 'Администрирование', 'Дизайн', 'Контент', 'Маркетинг', 'Разное']
    result_json = []
    index_of_categories = 0
    activated = []

    for category in categories:
        for page_number in range(1, 2):
            url = f'https://freelance.habr.com/freelancers?_=1671745232785&categories={category}page={page_number}'
            response = requests.get(url=url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')

            fl_info = soup.find('ul', id='freelancers_list').find_all('article', class_='user')

            for n in fl_info:

                els = n.find_all('li', class_='tags__item')
                exists = n.find('span', class_='user-profile__status_verified')

                for el in els:
                    activated.append(el.text.strip())

                result_json.append(
                    {
                        n.find('div', class_='user__info').find('a', href=True).text.replace('\n', ''):
                        {
                            'Имя специалиста': n.find('div', class_='user__info').find('a', href=True).text.replace('\n', ''),
                            'Статус аккаунта': str(['Аккаунт не верифицирован' if exists is None else n.find('span', class_='user-profile__status_verified').text.strip()]).translate({ord(i): None for i in "[]''"}),
                            'Сфера деятельности': categories_for_json[index_of_categories],
                            'Положительных отзывов': n.find('div', class_='user_rating').find('a', class_='positive', href=True).text.strip().replace('+', ''),
                            'Отрицательных отзывов:': n.find('div', class_='user_rating').find('a', class_='negative', href=True).text.strip().replace('-', ''),
                            'Специализация': n.find('div', class_='user-data__spec').text.strip(),
                            'Стоимость услуги': n.find('div', class_='user__price').text.strip(),
                            'Используемые технологии': str(activated).translate({ord(i): None for i in "[]''"}),
                        }

                    }
                )
                activated = []
        index_of_categories += 1

    with open('finally.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)

    # user_input = input('Введите имя автора: ')
    #
    # for x in result_json:
    #     if user_input in x:
    #         for key, value in x.get(user_input).items():
    #             print(key, ':', value)
    #         print(f'Информация актуальна на {datetime.now().strftime("%d.%m.%Y")}, {datetime.now().strftime("%H:%M:%S")}\n')
    #         is_showed = True
    # else:
    #     if is_showed is False:
    #         print('Данный автор либо не представлен на сайте, либо слишком неактивен!')
    #     else:
    #         pass


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == '__main__':
    main()
