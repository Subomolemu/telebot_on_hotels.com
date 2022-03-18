from loader import bot
from states.city_information import CityInfoState
from telebot.types import Message
from api import city_group, hotel_information, get_photos



@bot.message_handler(commands=['lowprice'])
def survey(message: Message) -> None:
    bot.set_state(user_id=message.from_user.id,
                  state=CityInfoState.qualifying_choice,
                  chat_id=message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название города')


@bot.message_handler(state=CityInfoState.qualifying_choice)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Пожалуйста, уточните ваш выбор')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for index, i_dict in enumerate(city_group.get_city_group(message.text)):
            for city_name in i_dict:
                bot.send_message(message.from_user.id, f'{index + 1}) {city_name}')
                data[city_name] = i_dict[city_name]
    bot.set_state(user_id=message.from_user.id,
                  state=CityInfoState.selected_city,
                  chat_id=message.chat.id)


@bot.message_handler(state=CityInfoState.selected_city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Введите количество отелей')
    bot.set_state(user_id=message.from_user.id,
                  state=CityInfoState.total_hotels,
                  chat_id=message.chat.id)
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['selected_city'] = message.text


@bot.message_handler(state=CityInfoState.total_hotels)
def get_total_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Выводить фотографии?')
        bot.set_state(user_id=message.from_user.id,
                      state=CityInfoState.photo_output,
                      chat_id=message.chat.id)
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['total_hotels'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество вводится цифрами')


@bot.message_handler(state=CityInfoState.photo_output)
def check_output(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == "Да":
            bot.send_message(message.from_user.id, 'Введите количество фотографий')
            bot.set_state(user_id=message.from_user.id,
                          state=CityInfoState.total_photos,
                          chat_id=message.chat.id)
        
        elif message.text == "Нет":
            bot.send_message(message.from_user.id, 'Выполняется поиск по заданным параметрам')
            dist_id = data[data['selected_city']]
            for i, date in enumerate(hotel_information.find_low_price(dist_id)):
                if i == int(data['total_hotels']):
                    break
                else:
                    address = f'{date["address"]["countryName"]}, {date["address"]["region"]}, ' \
                              f'{date["address"]["locality"]}, {date["address"]["streetAddress"]}'
                    text = f'{i + 1}) Название отеля: {date["name"]}\n' \
                           f'\tАдрес: {address}\n' \
                           f'\tРасстояние до центра: {date["landmarks"][0]["distance"]}\n' \
                           f'\tЦена: {date["ratePlan"]["price"]["current"]}\n'
                    bot.send_message(message.from_user.id, text)
        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, нажмите на кнопку (Да/Нет)')


@bot.message_handler(state=CityInfoState.total_photos)
def get_total_photos(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['total_photos'] = message.text
            bot.send_message(message.from_user.id, 'Выполняется поиск по заданным параметра:')
            dist_id = data[data['selected_city']]
            for i, date in enumerate(hotel_information.find_low_price(dist_id)):
                if i == int(data['total_hotels']):
                    break
                else:
                    address = f'{date["address"]["countryName"]}, {date["address"]["region"]}, ' \
                              f'{date["address"]["locality"]}, {date["address"]["streetAddress"]}'
                    text = f'{i + 1}) Название отеля: {date["name"]}\n' \
                           f'\tАдрес: {address}\n' \
                           f'\tРасстояние до центра: {date["landmarks"][0]["distance"]}\n' \
                           f'\tЦена: {date["ratePlan"]["price"]["current"]}\n'
                    bot.send_message(message.from_user.id, text)
                    
                    bot.send_media_group(message.from_user.id,
                                         get_photos.get_photos(date["id"],
                                                               data['total_photos']))

    else:
        bot.send_message(message.from_user.id, 'Количество вводится цифрами')
