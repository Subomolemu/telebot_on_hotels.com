import json
import re
from typing import List
from telebot.types import InputMediaPhoto
from config_data import config
from utils.misc.check_api import request_to_api


def get_photos(hotel_id, count) -> List:
    list_url = list()
    url_cite = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': config.RAPID_API_KEY}
    
    if request_to_api(url=url_cite, querystring=querystring, headers=headers):
        pattern = r'{"baseUrl":.+?.jpg"'
        find = re.findall(pattern, request_to_api(url=url_cite, querystring=querystring, headers=headers))
        if find:
            for i, photo_url in enumerate(find):
                date_photo = json.loads(photo_url + '}')
                if i < int(count):
                    cur_url_photo = re.sub(r'{size}', 'z', date_photo['baseUrl'])
                    list_url.append(InputMediaPhoto(cur_url_photo))
                else:
                    break
        return list_url

        