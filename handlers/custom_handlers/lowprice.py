from loader import bot
from states.city_information import CityInfoState
from telebot.types import Message
from api import city_group, hotel_information, get_photos
from keyboards import reply
from datetime import datetime, date
import re


@bot.message_handler(commands=['lowprice'])
def city(message: Message) -> None:
    bot.set_state(user_id=message.from_user.id,
                  state=CityInfoState.selected_city,
                  chat_id=message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название города')


@bot.message_handler(state=CityInfoState.selected_city)
def area(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for index, i_dict in enumerate(city_group.get_city_group(message.text)):
            for city_name in i_dict:
                data[city_name] = i_dict[city_name]
        data['city_name'] = message.text
        bot.send_message(message.from_user.id, 'Пожалуйста, уточните ваш выбор',
                         reply_markup=reply.areas.get_areas(message.text))

    bot.set_state(user_id=message.from_user.id,
                  state=CityInfoState.date_in,
                  chat_id=message.chat.id)


@bot.message_handler(state=CityInfoState.date_in)
def date_in(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text in data:
            data['dest_id'] = data[message.text]
            bot.send_message(message.from_user.id, 'Введите дату въезда\n'
                                                   'Пример введенный даты: 2022-01-31')
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.date_out,
                          chat_id=message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже',
                             reply_markup=reply.areas.get_areas(data['city_name']))


@bot.message_handler(state=CityInfoState.date_out)
def date_out(message: Message) -> None:
    try:
        date_pt = re.search(r'\d{4}-\d{2}-\d{2}', message.text)
        if date_pt.group():
            date_format = "%Y-%m-%d"
            now = date.today()
            selected_date_in = datetime.strptime(message.text, date_format).date()
            if selected_date_in < now:
                bot.send_message(message.from_user.id, f'Ошибка ввода\n'
                                                       f'Введите дату въезда не ранее чем {now}\n'
                                                       f'Пример введенный даты: 2022-01-31')
            else:
                bot.send_message(message.from_user.id, 'Введите дату выезда\n'
                                                       'Пример введенный даты: 2022-01-31')
                bot.set_state(user_id=message.from_user.id,
                              state=CityInfoState.total_hotels,
                              chat_id=message.chat.id)

                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['date_in'] = message.text
        else:
            bot.send_message(message.from_user.id, 'Ошибка ввода\n'
                                                   'Введите дату въезда\n'
                                                   'Пример введенный даты: 2022-01-31')
    except ValueError:
        bot.send_message(message.from_user.id, 'Ошибка значения даты\n'
                                               'Введите дату въезда\n'
                                               'Пример введенный даты: 2022-01-31\n'
                                               'Обратите внимание на количество месяцев и дней в выбранном месяце')


@bot.message_handler(state=CityInfoState.total_hotels)
def total_hotels(message: Message) -> None:
    try:
        date_pt = re.search(r'\d{4}-\d{2}-\d{2}', message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if date_pt.group():
                date_format = "%Y-%m-%d"
                selected_date_in = datetime.strptime(data['date_in'], date_format).date()
                selected_date_out = datetime.strptime(message.text, date_format).date()

                if selected_date_in >= selected_date_out:
                    bot.send_message(message.from_user.id, f'Ошибка ввода\n'
                                                           f'Введите дату выезда не ранее чем {selected_date_in}\n'
                                                           f'Пример введенный даты: 2022-01-31')
                else:
                    bot.send_message(message.from_user.id, 'Выберите количество отелей',
                                     reply_markup=reply.total_hotels.get_kb())
                    bot.set_state(user_id=message.from_user.id,
                                  state=CityInfoState.get_photos,
                                  chat_id=message.chat.id)
                    data['date_out'] = message.text
            else:
                bot.send_message(message.from_user.id, 'Ошибка ввода\n'
                                                       'Введите дату выезда\n'
                                                       'Пример введенный даты: 2022-01-31')
    except ValueError:
        bot.send_message(message.from_user.id, 'Ошибка значения даты\n'
                                               'Введите дату въезда\n'
                                               'Пример введенный даты: 2022-01-31\n'
                                               'Обратите внимание на количество месяцев и дней в выбранном месяце')


@bot.message_handler(state=CityInfoState.get_photos)
def ask_photo(message: Message) -> None:
    if message.text.isdigit() and message.text in ['3', '5', '9']:
        bot.send_message(message.from_user.id, 'Выводить фотографии?',
                         reply_markup=reply.out_photo.get_kb())
        bot.set_state(user_id=message.from_user.id,
                      state=CityInfoState.photo_output,
                      chat_id=message.chat.id)
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['total_hotels'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже',
                         reply_markup=reply.total_hotels.get_kb())


@bot.message_handler(state=CityInfoState.photo_output)
def answer_photo(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == "Да":
            bot.send_message(message.from_user.id, 'Выберите количество фотографий',
                             reply_markup=reply.total_photo.get_kb())
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.total_photos,
                          chat_id=message.chat.id)
        
        elif message.text == "Нет":
            bot.send_message(message.from_user.id, 'Выполняется поиск по заданным параметрам')
            dist_id = data['dest_id']
            for i, i_date in enumerate(hotel_information.find_low_price(dist_id, data['date_in'], data['date_out'])):
                if i == int(data['total_hotels']):
                    break
                else:
                    address = f'{i_date["address"]["countryName"]}, {i_date["address"]["region"]}, ' \
                              f'{i_date["address"]["locality"]}, {i_date["address"]["streetAddress"]}'
                    text = f'{i + 1}) Название отеля: {i_date["name"]}\n' \
                           f'\tАдрес: {address}\n' \
                           f'\tРасстояние до центра: {i_date["landmarks"][0]["distance"]}\n' \
                           f'\tЦена за сутки: {i_date["ratePlan"]["price"]["current"]}\n' \
                           f'\thttps://hotels.com/ho{i_date["id"]}'
                    bot.send_message(message.from_user.id, text)
        else:
            bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже', reply_markup=out_photo.get_kb())


@bot.message_handler(state=CityInfoState.total_photos)
def out_photo(message: Message) -> None:
    if message.text.isdigit() and message.text in [f'{i}' for i in range(1, 10)]:

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['total_photos'] = int(message.text)

            bot.send_message(message.from_user.id, 'Выполняется поиск по заданным параметра:')
            dist_id = data['dest_id']
            for i, i_date in enumerate(hotel_information.find_low_price(dist_id, data['date_in'], data['date_out'])):
                if i == int(data['total_hotels']):
                    break

                else:
                    address = f'{i_date["address"]["countryName"]}, {i_date["address"]["region"]}, ' \
                              f'{i_date["address"]["locality"]}, {i_date["address"]["streetAddress"]}'
                    text = f'{i + 1}) Название отеля: {i_date["name"]}\n' \
                           f'\tАдрес: {address}\n' \
                           f'\tРасстояние до центра: {i_date["landmarks"][0]["distance"]}\n' \
                           f'\tЦена за сутки: {i_date["ratePlan"]["price"]["current"]}\n' \
                           f'\thttps://hotels.com/ho{i_date["id"]}'

                    bot.send_message(message.from_user.id, text)
                    bot.send_media_group(message.from_user.id,
                                         get_photos.get_photos(i_date["id"],
                                                               data['total_photos']))

    else:
        bot.send_message(message.from_user.id, 'Просто нажмите на кнопку',
                         reply_markup=reply.total_photo.get_kb())
