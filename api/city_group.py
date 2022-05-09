import json
import re
from config_data import config
from utils.misc.check_api import request_to_api


def get_city_group(city):
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


