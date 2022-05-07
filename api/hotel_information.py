import requests
import json
import re
from requests.exceptions import ConnectTimeout
from config_data import config


def find_low_price(dest_id, date_in, date_out):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": dest_id, "pageNumber": "1", "pageSize": "25",
                   f"checkIn": {str(date_in)}, "checkOut": f"{str(date_out)}", "adults1": "1",
                   "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': config.RAPID_API_KEY}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            pattern = r'(?<="results":).+}{2}]'
            find = re.search(pattern, response.text)
            if find:
                res = json.loads(find[0])
                for date in res:
                    yield date
    except ConnectTimeout as exp:
        print(exp)
