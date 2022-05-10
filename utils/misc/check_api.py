from requests.exceptions import ConnectTimeout, ReadTimeout
import requests


def request_to_api(url, headers, querystring):
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.text
    except [ConnectTimeout, ReadTimeout]:
        return None
