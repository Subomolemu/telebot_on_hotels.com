from datetime import datetime


def days(day_in, day_out) -> int:
    """
    Функция, предназначенная для подсчета количества дней, которые пользователь проведет в отеле исходя
    из даты въезда и даты выезда, выбранных пользователем

    :param day_in: дата въезда, выбранная пользователем.
    :param day_out: дата выезда, выбранная пользователем.
    :return: возвращает количество дней которые пользователь проведет в отеле в виде числа
    """
    fmt = '%Y-%m-%d'
    fmt_day_in = datetime.strptime(day_in, fmt).date()
    fmt_day_out = datetime.strptime(day_out, fmt).date()
    find_day = (fmt_day_out - fmt_day_in).days
    return find_day
