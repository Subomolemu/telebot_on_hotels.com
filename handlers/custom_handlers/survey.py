from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message
from keyboards.reply.contact import request_contact


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(user_id=message.from_user.id,
                  state=UserInfoState.name,
                  chat_id=message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username}, введи свое имя')
    
    
@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, записал, теперь введи свой возраст')
        bot.set_state(user_id=message.from_user.id,
                      state=UserInfoState.age,
                      chat_id=message.chat.id)
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Имя должно состоять из букв')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал, теперь введи свою страну')
        bot.set_state(user_id=message.from_user.id,
                      state=UserInfoState.country,
                      chat_id=message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Возраст должен состоять из цифр')


@bot.message_handler(state=UserInfoState.country)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо, записал, теперь введи свой город')
    bot.set_state(user_id=message.from_user.id,
                  state=UserInfoState.city,
                  chat_id=message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо, записал. Отправь свой номер телефона, '
                                           'нажав на кнопку', reply_markup=request_contact())
    bot.set_state(user_id=message.from_user.id,
                  state=UserInfoState.phone_number,
                  chat_id=message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        

@bot.message_handler(content_types=['text', 'contack'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            text = f'Спасибо за предоставленную информацию, ваши данные:\n' \
                   f'    Имя - {data["name"]}\n' \
                   f'    Возраст - {data["age"]}\n' \
                   f'    Страна - {data["country"]}\n' \
                   f'    Город - {data["city"]}\n' \
                   f'    Номер телефона - {data["phone_number"]}'
            bot.send_message(message.from_user.id, text)
            
    else:
        bot.send_message(message.from_user.id, 'Отправьте номер телефона, нажав на кнопку')