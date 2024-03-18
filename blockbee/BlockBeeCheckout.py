"""
BlockBee's Checkout Python Helper
"""

import requests
from requests.models import PreparedRequest


class BlockBeeCheckoutHelper:
    BLOCKBEE_URL = 'https://api.blockbee.io/'
    BLOCKBEE_HOST = 'api.blockbee.io'

    def __init__(self, api_key, parameters=None, bb_params=None):
        if parameters is None:
            parameters = {}

        if bb_params is None:
            bb_params = {}

        if api_key is None:
            raise Exception("API Key Missing")

        self.parameters = parameters
        self.bb_params = bb_params
        self.api_key = api_key

    def payment_request(self, redirect_url, value):
        if redirect_url is None or value is None:
            return None

        if self.parameters:
            req = PreparedRequest()
            req.prepare_url(redirect_url, self.parameters)
            redirect_url = req.url

        params = {
            'redirect_url': redirect_url,
            'apikey': self.api_key,
            'value': value,
            **self.bb_params}

        _request = BlockBeeCheckoutHelper.process_request('', endpoint='checkout/request', params=params)
        if _request['status'] == 'success':
            return _request
        return None

    @staticmethod
    def payment_logs(token, api_key):
        if token is None or api_key is None:
            return None

        params = {
            'apikey': api_key,
            'token': token
        }

        _request = BlockBeeCheckoutHelper.process_request('', endpoint='checkout/logs', params=params)

        if _request['status'] == 'success':
            return _request
        return None

    def deposit_request(self, notify_url):
        if notify_url is None:
            return None

        if self.parameters:
            req = PreparedRequest()
            req.prepare_url(notify_url, self.parameters)
            notify_url = req.url

        params = {
            'notify_url': notify_url,
            'apikey': self.api_key,
            **self.bb_params}

        _request = BlockBeeCheckoutHelper.process_request('', endpoint='deposit/request', params=params)

        if _request['status'] == 'success':
            return _request
        return None

    @staticmethod
    def deposit_logs(token, api_key):
        if token is None or api_key is None:
            return None

        params = {
            'apikey': api_key,
            'token': token
        }

        _request = BlockBeeCheckoutHelper.process_request('', endpoint='deposit/logs', params=params)

        if _request['status'] == 'success':
            return _request
        return None

    @staticmethod
    def process_request(coin='', endpoint='', params=None):
        if coin != '':
            coin += '/'

        response = requests.get(
            url="{base_url}{coin}{endpoint}/".format(
                base_url=BlockBeeCheckoutHelper.BLOCKBEE_URL,
                coin=coin.replace('_', '/'),
                endpoint=endpoint,
            ),
            params=params,
            headers={'Host': BlockBeeCheckoutHelper.BLOCKBEE_HOST},
        )

        return response.json()
