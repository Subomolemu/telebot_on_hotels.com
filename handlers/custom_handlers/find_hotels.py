import re
from loader import bot
from states.city_information import CityInfoState
from telebot.types import Message
from api import city_group
from keyboards import reply
from datetime import datetime, date, timedelta
from telegram_bot_calendar import DetailedTelegramCalendar
from utils.misc import find_day, get_results
from database import db_add_info


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'],
                     func=lambda message: message not in ['/start', 'help'])
def city(message: Message) -> None:
    """
    Функция, предназначения для получения от пользователя названия города для поиска отеля.
    Записывает информацию об одной из введенной команде пользователем, таких как 'lowprice', 'highprice', 'bestdeal
    для корректировки сценария
    """
    bot.set_state(user_id=message.from_user.id,
                  state=CityInfoState.selected_city,
                  chat_id=message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название города')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
        data['command_date'] = str(datetime.utcfromtimestamp(message.date + 10800))


@bot.message_handler(state=CityInfoState.selected_city)
def area(message: Message) -> None:
    """
    Функция, предназначенная для уточнения выбора района поиска отелей пользователем.
    Записывает информацию о районах и их ид.

    Если ранее веденная команда пользователем является '/bestdeal' то выведет пользователь на сценарий,
    получающий от пользователя информация о минимальных и максимальных значения цены и удаленности отеля от центра,
    после этого выводит пользователя на календарь для выбора даты въезда и выезда

    Если ранее веденная команда пользователем является 'lowprice' или 'highprice' сразу выводит пользователя на
    календарь для выбора даты въезда и выезда
    """
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
    """
    Функция, предназначенная для выбора пользователем желаемого диапазона цен из предоставленного ботом списка.
    Записывает ид выбранного района поиска пользователем
    """
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
    """
    Функция, предназначенная для выбора пользователем желаемого диапазона удаленности отеля от центра в километрах
    из предоставленного ботом списка. Записывает информацию о диапазоне цен выбранного пользователем
    """
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
    """
    Функция - календарь, предназначенная для выбора пользователем желаемой даты въезда в отель. Дата выбирается
    начиная с текущей даты.

    Записывает информацию об ид отеля, если введенные пользователем команды для поиска
    являются 'lowprice' или 'highprice'
    Если командой от пользователя является '/bestdeal' то записывает информацию о выборе желаемого диапазона
    удаленности от центра для отелей в километрах
    """
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
    """
    Функция - календарь, предназначенная для выбора пользователем желаемой даты выезда из отеля. Выбор даты
    начинается с даты, следующей после выбранной пользователем желаемой даты въезда в отель

    Записывает информацию о выбранной пользователем дате въезда в отель
    """
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
    """
    Функция, предназначенная для выбора длины списка отелей из предложенных ботом вариантов

    Записывает выбранную пользователем дату выезда из отеля, и считает общее количество дней в отеле на основе
    выбранных пользователем дат въезда и выезда
    """
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
    """
    Функция, предназначенная для опроса пользователя с целью получения информации о том, нужно ли выводить фотографии
    отеля для пользователя

    Записывает информацию о выбранной пользователем длине списка отелей, который бот предоставит пользователю
    """
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
    """
    Функция, предназначенная для обработки ответа от пользователя о необходимости вывода фотографий отеля

    Если ответ от пользователя 'Да', то отправляет от пользователя информацию о длине списка фотографий отеля,
    которые отправит бот пользователю следующим сообщением после информации об отеле

    Если ответ от пользователя 'Нет', то начинает поиск отелей по собранной информации от пользователя без
    вывода ботом фотографий отеля
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == "Да":
            bot.send_message(message.from_user.id, 'Выберите количество фотографий',
                             reply_markup=reply.total_photo.get_kb())
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.total_photos,
                          chat_id=message.chat.id)

        elif message.text == "Нет":
            data['hotels'] = get_results.results(message=message, data=data, out_foto=False)
            if not data['hotels']:
                bot.send_message(message.from_user.id,
                                 f'Произошла ошибка, начните поиск снова. Текущая команда: \n{data["command"]}')
            db_add_info.add(user_id=data['user_id'], command_date=data['command_date'], command=data['command'],
                            hotels=data['hotels'])
        else:
            bot.send_message(message.from_user.id, 'Просто нажмите на кнопку',
                             reply_markup=reply.out_photo.get_kb())


@bot.message_handler(state=CityInfoState.total_photos)
def out_photo(message: Message) -> None:
    """
    Функция, предназначенная для поиска отелей по собранной от пользователя информации, если пользователь запросил
    вывод фотографий отеля

    По окончании поиска выводит сценарий на получение от пользователя следующего названия города для поиска
    результата по ранее веденной команде, либо попросит ввести новую команду
    """
    if message.text.isdigit() and message.text in [f'{i}' for i in range(1, 10)]:

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['total_photos'] = int(message.text)

            data['hotels'] = get_results.results(message=message, data=data, out_foto=True)
            if not data['hotels']:
                bot.send_message(message.from_user.id,
                                 f'Произошла ошибка, возможно стоит изменить параметры поиска, '
                                 f'начните поиска снова. Текущая команда: \n{data["command"]}')
            else:
                db_add_info.add(user_id=data['user_id'], command_date=data['command_date'], command=data['command'],
                                hotels=data['hotels'])
                bot.send_message(message.from_user.id, 'Вы можете ввести новую команду для поиска\n'
                                                       f'Текущая команда "{data["command"]}"\n'
                                                       f'Для получения справки -> "/help"')
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.end,
                          chat_id=message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Просто нажмите на кнопку',
                         reply_markup=reply.total_photo.get_kb())
