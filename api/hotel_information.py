import json
import re
from config_data import config
from utils.misc.check_api import request_to_api
from typing import Dict


def find_hotels(dest_id: str, date_in: str, date_out: str, sort_order: str,
                price_min: str = None, price_max: str = None, local_min: str = None, local_max: str = None,
                page_number: int = 1) -> Dict:
    """
    Функция для работы с апи на rapidapi.com сайта hotels.com
    Предназначена для получения информации об отелях в районе города по destination_id

    :param dest_id: id района города
    :param date_in: дата въезда в отель
    :param date_out: дата выезда из отеля
    :param sort_order: метод сортировки результатов для rapidapi.com сайта hotels.com
    :param price_min: значение минимальной цены для сортировки результат поиска
    :param price_max: значение максимальной цены для сортировки результат поиска
    :param local_min: значение минимального расстояния от центра города для сортировки результат поиска
    :param local_max: значение максимального расстояния от центра города для сортировки результат поиска
    :param page_number: номер страницы для вывода результатов поиска rapidapi.com сайта hotels.com
    :return: json с информацией об отеле
    """
    url_cite = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": dest_id, "pageNumber": page_number, "pageSize": "25",
                   f"checkIn": date_in, "checkOut": date_out, "adults1": "1",
                   "sortOrder": sort_order, "locale": "ru_RU", "currency": "RUB"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': config.RAPID_API_KEY}

    if price_min:
        querystring['priceMin'] = price_min
    if price_max:
        querystring['priceMax'] = price_max

    if request_to_api(url=url_cite, querystring=querystring, headers=headers):
        pattern = r'(?<="results":).+}{2}]'
        find = re.search(pattern, request_to_api(url=url_cite, querystring=querystring, headers=headers))
        if find:
            res = json.loads(find[0])
            for date in res:
                try:
                    distance = float(date["landmarks"][0]["distance"][:-2].replace(',', '.'))
                    lst_key = [date["address"]["countryName"], date["address"]["region"], date["address"]["locality"],
                               date["address"]["streetAddress"], date["name"], date["name"], date["id"],
                               date["ratePlan"]["price"]["current"], date["ratePlan"]["price"]["exactCurrent"]]
                    if local_min and local_max:
                        if not float(local_min) <= distance <= float(local_max):
                            continue
                    if not lst_key:
                        raise KeyError
                except KeyError:
                    continue
                yield date
