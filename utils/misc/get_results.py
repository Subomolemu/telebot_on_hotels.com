from api import hotel_information, get_photos
from loader import bot
from telebot.types import Message
from typing import Dict


def results(message: Message, data: Dict, sort_order: str = 'PRICE', out_foto: bool = False) -> None:
    """
    Функция, предназначенная, для поиска и вывода пользователю информации об отеле

    :param message: сообщение от пользователя в боте.
    :param data: словарь с информацией, собранной ботом от пользователя.
    :param sort_order: метод сортировки результатов вывода отелей по убыванию либо возрастанию цены.
    :param out_foto: True для вывода фото и False, если вывод фото не нужен
    """
    bot.send_message(message.from_user.id, 'Выполняется поиск по заданным параметрам:')
    dist_id = data['dest_id']
    if data['command'] == '/highprice':
        sort_order = 'PRICE_HIGHEST_FIRST'
    elif data['command'] in ['/bestdeal', '/lowprice']:
        sort_order = 'PRICE'
    page = 0
    can_iter = True
    total_hotels = int(data['total_hotels'])
    while can_iter:
        page += 1
        print('поиск на странице', page)
        bot.send_message(message.from_user.id, 'Пожалуйста, подождите')
        total_iter = (sum(1 for _ in hotel_information.find_hotels(dest_id=dist_id,
                                                                   date_in=data['date_in'],
                                                                   date_out=data['date_out'],
                                                                   price_min=data['min_price'],
                                                                   price_max=data['max_price'],
                                                                   local_min=data['min_local'],
                                                                   local_max=data['max_local'],
                                                                   sort_order=sort_order,
                                                                   page_number=page)))
        print('итераций на странице:', total_iter)
        if total_iter == 0:
            bot.send_message(message.from_user.id, 'Бот закончил поиск')
            break
        for i, i_date in enumerate(hotel_information.find_hotels(dest_id=dist_id,
                                                                 date_in=data['date_in'],
                                                                 date_out=data['date_out'],
                                                                 price_min=data['min_price'],
                                                                 price_max=data['max_price'],
                                                                 local_min=data['min_local'],
                                                                 local_max=data['max_local'],
                                                                 sort_order=sort_order,
                                                                 page_number=page)):

            if i == total_hotels:
                bot.send_message(message.from_user.id, 'Бот закончил поиск')
                can_iter = False
                break

            else:
                print(i_date)
                address = f'{i_date["address"]["countryName"]}, {i_date["address"]["region"]}, ' \
                          f'{i_date["address"]["locality"]}, {i_date["address"]["streetAddress"]}'
                full_price = data["all_day"] * int(i_date["ratePlan"]["price"]["exactCurrent"])
                edited_price = format(full_price, ',')
                text = f'{i + 1}) Название отеля: {i_date["name"]}\n' \
                       f'\tАдрес: {address}\n' \
                       f'\tРасстояние до центра: {i_date["landmarks"][0]["distance"]}\n' \
                       f'\tЦена за сутки: {i_date["ratePlan"]["price"]["current"]}\n' \
                       f'\tЦена за все время: {edited_price} RUB\n' \
                       f'\thttps://hotels.com/ho{i_date["id"]}'
                bot.send_message(message.from_user.id, text)
                if out_foto:
                    bot.send_media_group(message.from_user.id,
                                         get_photos.get_photos(i_date["id"],
                                                               int(data['total_photos'])))
            if total_iter < total_hotels:
                if i + 1 == total_iter:
                    total_hotels -= total_iter
