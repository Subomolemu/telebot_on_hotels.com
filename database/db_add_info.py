from . import main_db
from typing import List


def add(user_id: str, command_date: str, command: str, hotels: List) -> None:
    """
    Функция предназначена для записи следующей информации об истории поиска пользователем: дата ввода команды,
    сама команда, список найденных отелей. При этом в дб записывается информация только при успешной работе бота.
    :param user_id: ид пользователя
    :param command_date: время введенной команды от пользователя
    :param command: команда, введенная пользователем
    :param hotels: список полученных отелей
    """
    hotels = '\n- ' + '\n- '.join(hotels)
    with main_db.db:
        main_db.Info.create(user_id=user_id, command_time=command_date, command=command, hotels=hotels)
