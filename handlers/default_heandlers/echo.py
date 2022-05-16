from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """
    Функция предназначена для обработки сообщения от пользователя без состояния или фильтра или неизвестной команды
    """
    bot.reply_to(message, "Эхо без состояния или фильтра. Для получения справки по работе бота введите '/help' "
                          "или начните работу с ботом командой '/start'\nВаше сообщение:"
                          f"{message.text}")
