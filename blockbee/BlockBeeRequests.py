import requests
import json

from urllib.parse import urljoin, urlencode
from requests.exceptions import RequestException


class BlockBeeAPIException(Exception):
    pass


class BlockBeeRequests:
    BLOCKBEE_URL = 'https://api.blockbee.io/'
    BLOCKBEE_HOST = 'api.blockbee.io'

    @staticmethod
    def process_request_get(coin=None, endpoint='', params=None):
        if coin:
            coin += '/'
        else:
            coin = ''

        response = requests.get(
            url="{base_url}{coin}{endpoint}/".format(
                base_url=BlockBeeRequests.BLOCKBEE_URL,
                coin=coin.replace('_', '/'),
                endpoint=endpoint,
            ),
            params=params,
            headers={'Host': BlockBeeRequests.BLOCKBEE_HOST},
        )

        response_obj = response.json()

        if response_obj.get('status') == 'error':
            raise BlockBeeAPIException(response_obj['error'])

        return response_obj

    @staticmethod
    def process_request_post(coin=None, endpoint='', apiKey='', body=None, isJson=False):
        if coin:
            coin_path = coin.replace('_', '/') + '/'
        else:
            coin_path = ''

        url = urljoin(BlockBeeRequests.BLOCKBEE_URL, f"{coin_path}{endpoint}/")
        url += '?' + urlencode({'apikey': apiKey})

        headers = {
            'Host': BlockBeeRequests.BLOCKBEE_HOST,
        }

        if isJson:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(body)
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            data = urlencode(body)

        response = requests.post(url, headers=headers, data=data)

        response_obj = response.json()

        if response_obj.get('status') == 'error':
            raise BlockBeeAPIException(response_obj['error'])

        return response_obj