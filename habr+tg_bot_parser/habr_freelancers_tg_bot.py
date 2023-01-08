from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json


dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def get_all_authors(message: types.Message):
    await message.answer(
        text="<code>Привет!\nЯ помогу тебе узнать <b>автора</b> твоего заказа поподробнее."
             "\nПришли мне имя исполнителя, про которого хочешь получить информацию!</code>",
        parse_mode="HTML")


@dp.message_handler()
async def send_info(message: types.Message):
    m = message.text

    is_showed = False

    with open('result_asyncio.json') as f:
        authors_dict = json.load(f)

    for x in authors_dict:
        if m in x:
            s_name = x[m]['Имя автора']
            s_url = x[m]['Ссылка на профиль мастера']
            s_field = x[m]['Сфера деятельности']
            s_spet = x[m]['Специализация']
            s_pos = x[m][f'Позиция в категории «{s_field}»']

            res = f'<b>Информация актуальна на {datetime.now().strftime("%d.%m.%Y")}, {datetime.now().strftime("%H:%M:%S")}\n</b>' \
                  f"<code>\nИмя специалиста: {s_name}\n</code>" \
                  f"<code>\nСфера деятельности: {s_field}\n</code>" \
                  f"<code>\nСпециализация: {s_spet}\n</code>" \
                  f"<code>\nПозиция в категории «{s_field}»: {s_pos}\n</code>" \
                  f"<code>\nСсылка на профиль:</code>\n{s_url}\n" \

            await message.answer(res, parse_mode='HTML')

            is_showed = True

    else:
        if is_showed is False:
            no_info = f'<code>Данный автор либо не представлен на сайте, либо слишком неактивен!\nПопробуй снова!</code>'
            await message.answer(no_info, parse_mode='HTML')
        else:
            pass


if __name__ == '__main__':
    executor.start_polling(dp)
