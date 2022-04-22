from api import city_group
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_areas(city):
    keyboard = ReplyKeyboardMarkup(True, True)
    for area_dict in city_group.get_city_group(city):
        for area in area_dict.keys():
            button = KeyboardButton(text=f'{area}')
            keyboard.add(button)
    return keyboard
