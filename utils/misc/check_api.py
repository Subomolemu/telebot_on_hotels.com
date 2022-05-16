from requests.exceptions import ConnectTimeout, ReadTimeout
from urllib3.exceptions import ReadTimeoutError
import requests


def request_to_api(url, headers, querystring) -> (str, None):
    """
    Функция, предназначенная для проверки статуса запроса и отлова ошибок

    :param url: получает url сайта
    :param headers: сайт с апи и ключ к сайту
    :param querystring: условия и сортировка для запроса к апи
    :return: возвращает строку по requset если статус ответа без ошибок, либо 'None' если произошла ошибка
    """
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.text
    except (ConnectTimeout, ReadTimeout, ReadTimeoutError, TypeError) as err:
        print(type(err), err)
        return None
