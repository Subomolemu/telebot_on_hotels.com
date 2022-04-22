from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_kb():
    keyboard = ReplyKeyboardMarkup(True, True)
    kb_1 = KeyboardButton(text='1')
    kb_2 = KeyboardButton(text='2')
    kb_3 = KeyboardButton(text='3')
    kb_4 = KeyboardButton(text='4')
    kb_5 = KeyboardButton(text='5')
    kb_6 = KeyboardButton(text='6')
    kb_7 = KeyboardButton(text='7')
    kb_8 = KeyboardButton(text='8')
    kb_9 = KeyboardButton(text='9')
    keyboard.add(kb_1, kb_2, kb_3, kb_4, kb_5, kb_6, kb_7, kb_8, kb_9)
    return keyboard
