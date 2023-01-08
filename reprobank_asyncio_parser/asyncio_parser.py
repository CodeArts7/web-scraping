import asyncio
from bs4 import BeautifulSoup
import aiohttp
import json
import time


result_json = []
parameters = ['Рост', 'Глаза', 'Волосы', 'Группа крови']
start_time = time.time()


async def get_page_data(session, page_number):

    headers = {
        'user-agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) '
                      'Chrome / 108.0.0.0 Safari / 537.36',
        'accept': '*/*',
    }

    async with session.get(url=f'https://reprobank.ru/bank-donorov/katalog-donorov-spermi/?d_page={page_number}',
                           headers=headers, ssl=False) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")

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


async def gather_gotten_data():

    tasks = []

    async with aiohttp.ClientSession() as session:
        for page_number in range(1, 11):
            task = asyncio.create_task(get_page_data(session, page_number))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_gotten_data())

    with open('result_asyncio.json', 'w') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)

    finish_time = time.time() - start_time
    print(finish_time)


if __name__ == '__main__':
    main()
