import json
import re
from config_data import config
from utils.misc.check_api import request_to_api


def find_low_price(dest_id, date_in, date_out, sort_order):
    url_cite = "https://hotels4.p.rapidapi.com/properties/list"
    page_number = 1
    querystring = {"destinationId": dest_id, "pageNumber": page_number, "pageSize": "25",
                   f"checkIn": {str(date_in)}, "checkOut": f"{str(date_out)}", "adults1": "1",
                   "sortOrder": sort_order, "locale": "ru_RU", "currency": "RUB"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': config.RAPID_API_KEY}
    if request_to_api(url=url_cite, querystring=querystring, headers=headers):
        pattern = r'(?<="results":).+}{2}]'
        find = re.search(pattern, request_to_api(url=url_cite, querystring=querystring, headers=headers))
        if find:
            res = json.loads(find[0])
            for date in res:
                try:
                    lst_key = [date["address"]["countryName"], date["address"]["region"], date["address"]["locality"],
                               date["address"]["streetAddress"], date["name"], date["name"], date["id"],
                               date["landmarks"][0]["distance"], date["ratePlan"]["price"]["current"],
                               date["ratePlan"]["price"]["exactCurrent"]]
                    if not lst_key:
                        raise KeyError
                except KeyError:
                    continue
                yield date

