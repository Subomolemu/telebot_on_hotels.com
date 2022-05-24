from . import main_db
from datetime import date, datetime


def out(user_id: int) -> str:
    """
    Фукция предназначена для создания генератора вывода истории поиска пользователю. История выдается только за
    текущую дату. Вызывается при команде /history от пользователя.
    :param user_id: ид пользователя
    :return: выводт строку истории поиска, содержащую информацию о дате ввода команды, самой команде, списком найденных
    по запросу отелей.
    """
    with main_db.db:
        for i in main_db.Info.select().order_by(main_db.Info.user_id):
            if i.user_id == str(user_id) and date.today() == \
                    datetime.strptime(i.command_time, "%Y-%m-%d %H:%M:%S").date():
                yield f'{i.command_time}, "{i.command}", \nCписок найденных отелей: {i.hotels}'
