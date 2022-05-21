from telebot.types import Message, ReplyKeyboardRemove

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Функция, предназначенная для обработки команды '/start'от пользователя
    """
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                          f"Нажми на /help для получения информации о боте", reply_markup=ReplyKeyboardRemove())

