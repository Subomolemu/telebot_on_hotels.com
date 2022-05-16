from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def take_local() -> ReplyKeyboardMarkup:
    """
    Функция, предназначенная для вывода Reply клавиатуры с уточняющим выбором диапазона удаленности отелей от центра

    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(True, True)
    kb_1 = KeyboardButton(text='0 - 1')
    kb_2 = KeyboardButton(text='1 - 3')
    kb_3 = KeyboardButton(text='3 - 8')
    kb_4 = KeyboardButton(text='8 - 15')
    kb_5 = KeyboardButton(text='15 и более')
    keyboard.add(kb_1, kb_2, kb_3, kb_4, kb_5)
    return keyboard
