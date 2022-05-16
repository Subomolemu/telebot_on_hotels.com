import json
import re
from config_data import config
from utils.misc.check_api import request_to_api
from typing import Dict


def get_city_group(city: str) -> Dict:
    """
    Функция для работы с апи на rapidapi.com сайта hotels.com

    Предназначена для уточнения района поиска по введенному пользователем названию города

    :param city: название города, введенное пользователем.
    :return: генерирует словарь для уточнения места поиска отелей (ключ: название места; значение: ид места)
    """
    url_cite = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {f"query": city, "locale": "ru_RU"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': config.RAPID_API_KEY}
    if request_to_api(url=url_cite, querystring=querystring, headers=headers):
        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, request_to_api(url=url_cite, querystring=querystring, headers=headers))
        if find:
            json_city_group = json.loads(f"{{{find[0]}}}")
            for name in json_city_group['entities']:
                yield {name['name']: name['destinationId']}
