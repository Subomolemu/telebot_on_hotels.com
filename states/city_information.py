from telebot.handler_backends import State, StatesGroup


class CityInfoState(StatesGroup):
    selected_city = State()
    qualifying_choice = State()
    date_in = State()
    date_out = State()
    total_hotels = State()
    total_photos = State()
    get_photos = State()
    photo_output = State()
