from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def take_price() -> ReplyKeyboardMarkup:
    """
    Функция, предназначенная для вывода Reply клавиатуры с уточняющим выбором цен отелей

    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(True, True)
    kb_1 = KeyboardButton(text='0 - 4999')
    kb_2 = KeyboardButton(text='5000 - 9999')
    kb_3 = KeyboardButton(text='10000 - 29999')
    kb_4 = KeyboardButton(text='30000 - 79999')
    kb_5 = KeyboardButton(text='80000 - 149999')
    kb_6 = KeyboardButton(text='150000 и более')
    keyboard.add(kb_1, kb_2, kb_3, kb_4, kb_5, kb_6)
    return keyboard