from loader import bot
from telebot.types import Message, ReplyKeyboardRemove
from database import db_out_info


@bot.message_handler(commands=['history'])
def take_history(message: Message) -> None:
    """
    Функция предназначена для обработки команды /history от пользователя и вывода истории поиска.
    :param message: сообщение от пользователя боту
    """
    for msg in db_out_info.out(message.from_user.id):
        bot.send_message(message.from_user.id, msg)
    bot.send_message(message.from_user.id, 'Конец вывода истории', reply_markup=ReplyKeyboardRemove())
