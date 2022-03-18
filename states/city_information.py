from telebot.handler_backends import State, StatesGroup


class CityInfoState(StatesGroup):
    selected_city = State()
    qualifying_choice = State()
    total_hotels = State()
    total_photos = State()
    photo_output = State()