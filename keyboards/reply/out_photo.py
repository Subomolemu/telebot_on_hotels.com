from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_kb() -> ReplyKeyboardMarkup:
    """
    Функция, предназначенная для вывода Reply клавиатуры с уточняющим выбором от пользователя о необходимости вывода
    фотографий отеля

    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(True, True)
    kb_1 = KeyboardButton(text='Да')
    kb_2 = KeyboardButton(text='Нет')
    keyboard.add(kb_1, kb_2)
    return keyboard
