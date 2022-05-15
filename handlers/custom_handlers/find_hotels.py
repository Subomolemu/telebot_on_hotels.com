import re
from loader import bot
from states.city_information import CityInfoState
from telebot.types import Message
from api import city_group
from keyboards import reply
from datetime import datetime, date, timedelta
from telegram_bot_calendar import DetailedTelegramCalendar
from utils.misc import find_day, get_results


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def city(message: Message) -> None:

    bot.set_state(user_id=message.from_user.id,
                  state=CityInfoState.selected_city,
                  chat_id=message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название города')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text


@bot.message_handler(state=CityInfoState.selected_city)
def area(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for index, i_dict in enumerate(city_group.get_city_group(message.text)):
            for city_name in i_dict:
                data[city_name] = i_dict[city_name]
        data['city_name'] = message.text
        data['user_id'] = message.from_user.id
        bot.send_message(message.from_user.id, 'Пожалуйста, уточните ваш выбор',
                         reply_markup=reply.areas.get_areas(message.text))

        if data['command'] == '/bestdeal':
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.min_max_price,
                          chat_id=message.chat.id)
        else:
            data['min_price'] = None
            data['max_price'] = None
            data['min_local'] = None
            data['max_local'] = None
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.date_in,
                          chat_id=message.chat.id)


@bot.message_handler(state=CityInfoState.min_max_price)
def take_price(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text in data:
            data['dest_id'] = data[message.text]
            bot.send_message(message.from_user.id, 'Выберите желаемый диапазон цен в рублях:',
                             reply_markup=reply.min_max_price.take_price())
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.min_max_local,
                          chat_id=message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже',
                             reply_markup=reply.areas.get_areas(data['city_name']))


@bot.message_handler(state=CityInfoState.min_max_local)
def take_local(message: Message) -> None:
    fmt = r'\d+'
    find_price = re.findall(fmt, message.text)
    price_list = ['0', '4999', '5000', '9999', '10000', '29999', '30000', '79999', '80000', '149999']

    if len(find_price) == 2 or len(find_price) == 1:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if len(find_price) == 2:
                if (find_price[0] in price_list) and (find_price[1] in price_list) and \
                        (int(find_price[0]) < int(find_price[1])):
                    data['min_price'] = find_price[0]
                    data['max_price'] = find_price[1]

                    bot.send_message(message.from_user.id,
                                     'Выберите желаемый диапазон расстояния от центра в километрах:',
                                     reply_markup=reply.min_max_local.take_local())
                    bot.set_state(user_id=message.from_user.id,
                                  state=CityInfoState.date_in,
                                  chat_id=message.chat.id)
                else:
                    bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже',
                                     reply_markup=reply.min_max_price.take_price())

            elif len(find_price) == 1:
                if find_price[0] == 15000:
                    data['min_price'] = find_price[0]
                    data['max_price'] = 1e15

                    bot.send_message(message.from_user.id,
                                     'Выберите желаемый диапазон расстояния от центра в километрах:',
                                     reply_markup=reply.min_max_local.take_local())
                    bot.set_state(user_id=message.from_user.id,
                                  state=CityInfoState.date_in,
                                  chat_id=message.chat.id)
                else:
                    bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже',
                                     reply_markup=reply.min_max_price.take_price())

    else:
        bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже',
                         reply_markup=reply.min_max_price.take_price())


@bot.message_handler(state=CityInfoState.date_in)
def date_in(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        if message.text in data:
            data['dest_id'] = data[message.text]
            data['min_date'] = str(date.today())
            calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                                      min_date=date.today(),
                                                      locale='ru').build()
            bot.send_message(message.from_user.id, f"Выбираем дату", reply_markup=calendar)
        else:
            if data['command'] == '/bestdeal':
                fmt = r'\d+'
                find_local = re.findall(fmt, message.text)
                local_list = ['0', '1', '3', '8', '15']
                if len(find_local) == 2 or len(find_local) == 1:

                    if len(find_local) == 2:
                        if (find_local[0] in local_list) and (find_local[1] in local_list) and \
                                (int(find_local[0]) < int(find_local[1])):
                            data['min_local'] = find_local[0]
                            data['max_local'] = find_local[1]

                            data['min_date'] = str(date.today())
                            calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                                                      min_date=date.today(),
                                                                      locale='ru').build()
                            bot.send_message(message.from_user.id, f"Выбираем дату", reply_markup=calendar)
                        else:
                            bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже1',
                                             reply_markup=reply.min_max_local.take_local())

                    elif len(find_local) == 1:
                        if find_local[0] == '15':
                            data['min_local'] = find_local[0]
                            data['max_local'] = 1e15

                            data['min_date'] = str(date.today())
                            calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                                                      min_date=date.today(),
                                                                      locale='ru').build()
                            bot.send_message(message.from_user.id, f"Выбираем дату", reply_markup=calendar)
                        else:
                            bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже2',
                                             reply_markup=reply.min_max_local.take_local())
                else:
                    bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже3',
                                     reply_markup=reply.min_max_local.take_local())

            else:
                bot.send_message(message.from_user.id, 'Просто нажмите на кнопку ниже4',
                                 reply_markup=reply.areas.get_areas(data['city_name']))


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1),
                            state=CityInfoState.date_in)
def date_out(call) -> None:
    result, key, step = DetailedTelegramCalendar(calendar_id=1, min_date=date.today(), locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выбираем дату",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Даты въезда: {result}",
                              call.message.chat.id,
                              call.message.message_id)
        with bot.retrieve_data(call.message.chat.id) as data:
            data['date_in'] = str(result)
            bot.set_state(user_id=data['user_id'],
                          state=CityInfoState.date_out,
                          chat_id=call.message.chat.id)
            calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                                      min_date=datetime.strptime(data['date_in'], "%Y-%m-%d").date(),
                                                      locale='ru').build()
            bot.send_message(call.from_user.id, f"Выбираем дату", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2),
                            state=CityInfoState.date_out)
def total_hotels(call) -> None:
    with bot.retrieve_data(call.message.chat.id) as data:
        select_date = datetime.strptime(data['date_in'], "%Y-%m-%d").date() + timedelta(days=1)
        result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                     min_date=select_date,
                                                     locale='ru').process(
            call.data)
        if not result and key:
            bot.edit_message_text(f"Выбираем дату",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            data['date_out'] = str(result)
            data['all_day'] = find_day.days(day_in=data['date_in'], day_out=data['date_out'])
            bot.edit_message_text(f"Дата выезда: {result}",
                                  call.message.chat.id,
                                  call.message.message_id)
            bot.send_message(call.message.chat.id, 'Выберите количество отелей',
                             reply_markup=reply.total_hotels.get_kb())
            bot.set_state(user_id=data['user_id'],
                          state=CityInfoState.get_photos,
                          chat_id=call.message.chat.id)


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
            get_results.results(message=message, data=data)
        else:
            bot.send_message(message.from_user.id, 'Просто нажмите на кнопку',
                             reply_markup=reply.out_photo.get_kb())


@bot.message_handler(state=CityInfoState.total_photos)
def out_photo(message: Message) -> None:
    if message.text.isdigit() and message.text in [f'{i}' for i in range(1, 10)]:

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['total_photos'] = int(message.text)

            get_results.results(message=message, data=data, flag=True)

    else:
        bot.send_message(message.from_user.id, 'Просто нажмите на кнопку',
                         reply_markup=reply.total_photo.get_kb())
