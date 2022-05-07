import requests
import json
import re
from typing import List
from telebot.types import InputMediaPhoto
from requests.exceptions import ConnectTimeout
from config_data import config


def get_photos(hotel_id, count) -> List:
    list_url = list()
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': config.RAPID_API_KEY}
    
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            pattern = r'{"baseUrl":.+?.jpg"'
            find = re.findall(pattern, response.text)
            if find:
                for i, photo_url in enumerate(find):
                    date_photo = json.loads(photo_url + '}')
                    if i < int(count):
                        cur_url_photo = re.sub(r'{size}', 'z', date_photo['baseUrl'])
                        list_url.append(InputMediaPhoto(cur_url_photo))
                    else:
                        break
            return list_url
    except ConnectTimeout as exp:
        print(exp)
        