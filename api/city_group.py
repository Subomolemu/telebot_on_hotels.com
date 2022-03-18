import requests
import json
import re


def get_city_group(city):
    url_cite = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {f"query": city, "locale": "ru_RU"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': "2c1b5f4d5fmsh8f0f682bedda6c4p144119jsnae88caba9b7c"}
    try:
        response = requests.request("GET", url_cite, headers=headers, params=querystring)
        if response.status_code == requests.codes.ok:
            pattern = r'(?<="CITY_GROUP",).+?[\]]'
            find = re.search(pattern, response.text)
            if find:
                json_city_group = json.loads(f"{{{find[0]}}}")
                for name in json_city_group['entities']:
                    yield {name['name']: name['destinationId']}

    except Exception as exp:
        print(exp)