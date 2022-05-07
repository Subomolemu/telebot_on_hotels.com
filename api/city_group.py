import requests
import json
import re
from requests.exceptions import ConnectTimeout
from config_data import config

def get_city_group(city):
    url_cite = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {f"query": city, "locale": "ru_RU"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': config.RAPID_API_KEY}
    try:
        response = requests.request("GET", url_cite, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            pattern = r'(?<="CITY_GROUP",).+?[\]]'
            find = re.search(pattern, response.text)
            if find:
                json_city_group = json.loads(f"{{{find[0]}}}")
                for name in json_city_group['entities']:
                    yield {name['name']: name['destinationId']}

    except ConnectTimeout as exp:
        print(exp)
