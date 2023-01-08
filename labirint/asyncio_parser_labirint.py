import asyncio
import json
from bs4 import BeautifulSoup
import time
import aiohttp


start_time = time.time()
books_data = []


async def get_page_info(session, page_number):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    url = f'https://www.labirint.ru/genres/2308/?display=table&page={page_number}'
    async with session.get(url=url, headers=headers, ssl=False) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')

        book_items = soup.find('tbody', class_='products-table__body').find_all('tr')

        for bi in book_items:
            book_data = bi.find_all('td')
            # print(book_data)
            try:
                book_title = book_data[0].find('a').text.strip()
                book_link = f"https://www.labirint.ru{book_data[0].find('a').get('href').strip()}"
            except AttributeError:
                book_title = 'Нет названия книги'

            try:
                book_autor = book_data[1].text.strip()
            except AttributeError:
                book_autor = 'Автор не указан'

            try:
                book_pubhouse = book_data[2].find_all('a')
                book_pubhouse = ':'.join(bp.text for bp in book_pubhouse)
            except AttributeError:
                book_autor = 'Издательство не указан'

            try:
                book_amount = int(book_data[3].find('span', 'price-val').find('span').text.replace(' ', ''))

            except AttributeError:
                continue

            try:
                book_old_amount = int(book_data[3].find('span', 'price-old').find('span').text.strip().replace(' ', ''))
            except AttributeError:
                continue

            try:
                discount = round(100 - (book_amount * 100 / book_old_amount))
            except AttributeError:
                continue

            try:
                book_status = book_data[-1].text.strip()
            except AttributeError:
                book_status = 'Статус отсутствует'

            books_data.append(
                {
                    'name': book_title,
                    'autor': book_autor,
                    'publisher': book_pubhouse,
                    'amount': book_amount,
                    'olda_mount': book_old_amount,
                    'discount': discount,
                    'status': book_status,
                    'link': book_link,

                }
            )


async def gather_tasks():

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_number in range(1, 17):
            task = asyncio.create_task(get_page_info(session, page_number))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_tasks())
    with open('json_file.json', 'w') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)
    finish_time = time.time() - start_time
    print(finish_time)


if __name__ == '__main__':
    main()