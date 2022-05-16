from telebot.handler_backends import State, StatesGroup


class CityInfoState(StatesGroup):
    """
    Класс состояния пользователя для прохождения сценария
    """
    selected_city = State()
    qualifying_choice = State()
    min_max_price = State()
    min_max_local = State()
    date_in = State()
    date_out = State()
    total_hotels = State()
    total_photos = State()
    get_photos = State()
    photo_output = State()
