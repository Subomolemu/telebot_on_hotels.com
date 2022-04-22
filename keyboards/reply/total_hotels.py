from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_kb():
    keyboard = ReplyKeyboardMarkup(True, True)
    kb_1 = KeyboardButton(text='3')
    kb_2 = KeyboardButton(text='5')
    kb_3 = KeyboardButton(text='9')
    keyboard.add(kb_1, kb_2, kb_3)
    return keyboard
