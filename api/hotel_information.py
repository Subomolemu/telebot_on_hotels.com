import requests
import json


def find_low_price(dest_id, date_in, date_out):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": dest_id, "pageNumber": "1", "pageSize": "25",
                   f"checkIn": {str(date_in)}, "checkOut": f"{str(date_out)}", "adults1": "1",
                   "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': "2c1b5f4d5fmsh8f0f682bedda6c4p144119jsnae88caba9b7c"}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            jsons = json.loads(response.text)
            res = jsons['data']['body']['searchResults'].get('results')
            for date in res:
                yield date
    except Exception as exp:
        print(exp)