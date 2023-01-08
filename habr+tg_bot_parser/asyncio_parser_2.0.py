from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
import time


start_time = time.time()
result_json = []


async def get_page_data(session, category, page_number, index_of_categories):
    activated = []

    categories_for_json = ['Разработка', 'Тестирование', 'Администрирование',
                           'Дизайн', 'Контент', 'Маркетинг', 'Разное']

    headers = {
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.106 Safari/537.36",
        'accept': '*/*',
    }

    url = f'https://freelance.habr.com/freelancers?_=1671745232785&categories={category}page={page_number}'

    async with session.get(url=url, headers=headers, ssl=False) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")

        try:

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

            finish_time = time.time() - start_time
            print(f"{finish_time}")
        except AttributeError:
            pass


async def gather_data():
    index_of_categories = 0

    pagination_page = []
    number = 0

    headers = {
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.106 Safari/537.36",
        'accept': '*/*',
    }

    categories = [
        'development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other&',
        'testing_sites%2Ctesting_mobile%2Ctesting_software&',
        'admin_servers%2Cadmin_network%2Cadmin_databases%2Cadmin_security%2Cadmin_other&',
        'design_sites%2Cdesign_landings%2Cdesign_logos%2Cdesign_illustrations%2Cdesign_mobile%2Cdesign_icons%2Cdesign_polygraphy%2Cdesign_banners%2Cdesign_graphics%2Cdesign_corporate_identity%2Cdesign_presentations%2Cdesign_modeling%2Cdesign_animation%2Cdesign_photo%2Cdesign_other&',
        'content_copywriting%2Ccontent_rewriting%2Ccontent_audio%2Ccontent_article%2Ccontent_scenarios%2Ccontent_naming%2Ccontent_correction%2Ccontent_translations%2Ccontent_coursework%2Ccontent_specification%2Ccontent_management%2Ccontent_other&',
        'marketing_smm%2Cmarketing_seo%2Cmarketing_context%2Cmarketing_email%2Cmarketing_research%2Cmarketing_sales%2Cmarketing_pr%2Cmarketing_other&',
        'other_audit_analytics%2Cother_consulting%2Cother_jurisprudence%2Cother_accounting%2Cother_audio%2Cother_video%2Cother_engineering%2Cother_other&',
        ]

    async with aiohttp.ClientSession() as session:
        tasks = []

        for category in categories:

            async with session.get(url=f'https://freelance.habr.com/freelancers?_=1671745232785&categories={category}page=1', headers=headers, ssl=False) as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, "lxml")

                pagination = soup.find('div', class_='pagination').find_all('a', href=True)[-2]

                for pag in pagination:
                    pagination_page.append(int(pag.text.strip()))

            for page_number in range(1, pagination_page[number]):
                task = asyncio.create_task(get_page_data(session, category, page_number, index_of_categories))
                tasks.append(task)
            index_of_categories += 1
        number += 1

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())

    with open('result_asyncio.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)

    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == '__main__':
    main()