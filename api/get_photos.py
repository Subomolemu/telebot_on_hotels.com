import requests
import json
import re
from typing import List
from telebot.types import InputMediaPhoto


def get_photos(hotel_id, count) -> List:
    list_url = list()
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': "2c1b5f4d5fmsh8f0f682bedda6c4p144119jsnae88caba9b7c"}
    
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == requests.codes.ok:
            date_photo = json.loads(response.text)
            total_photo = date_photo['hotelImages']
            for i, photo_url in enumerate(total_photo):
                if i < int(count):
                    cur_url_photo = re.sub(r'{size}', 'z', photo_url['baseUrl'])
                    list_url.append(InputMediaPhoto(cur_url_photo))
        return list_url
    except Exception as exp:
        print(exp)
        