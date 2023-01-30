"""
BlockBee's Python Helper
"""

import requests
from requests.models import PreparedRequest


class Helper:
    BLOCKBEE_URL = 'https://api.blockbee.io/'
    BLOCKBEE_HOST = 'api.blockbee.io'

    def __init__(self, coin, own_address, callback_url, parameters, bb_params, api_key):
        if parameters is None:
            parameters = {}

        if bb_params is None:
            bb_params = {}

        if api_key is None:
            raise Exception("API Key Missing")

        self.coin = coin
        self.own_address = own_address
        self.callback_url = callback_url
        self.parameters = parameters
        self.bb_params = bb_params
        self.api_key = api_key
        self.payment_address = ''

    def get_address(self):
        if self.coin is None:
            return None

        coin = self.coin

        if self.parameters:
            req = PreparedRequest()
            req.prepare_url(self.callback_url, self.parameters)
            self.callback_url = req.url

        params = {
            'callback': self.callback_url,
            'apikey': self.api_key,
            **self.parameters, **self.bb_params}

        if self.own_address is not None:
            params['address'] = self.own_address

        _address = Helper.process_request(coin, endpoint='create', params=params)
        if _address:
            self.payment_address = _address['address_in']
            return _address

        return None

    def get_logs(self):
        coin = self.coin
        callback_url = self.callback_url

        if coin is None or callback_url is None:
            return None

        if self.parameters:
            req = PreparedRequest()
            req.prepare_url(self.callback_url, self.parameters)
            self.callback_url = req.url

        params = {
            'callback': callback_url,
            'apikey': self.api_key
        }

        _logs = Helper.process_request(coin, endpoint='logs', params=params)

        if _logs:
            return _logs

        return None

    def get_qrcode(self, value='', size=300):
        if self.coin is None:
            return None

        params = {
            'address': self.payment_address,
            'size': size,
            'apikey': self.api_key
        }

        if value:
            params['value'] = value

        _qrcode = Helper.process_request(self.coin, endpoint='qrcode', params=params)

        if _qrcode:
            return _qrcode

        return None

    def get_conversion(self, from_coin, value, api_key):
        if api_key is None:
            raise Exception("API Key Missing")

        params = {
            'from': from_coin,
            'value': value,
            'apikey': api_key
        }

        _value = Helper.process_request(self.coin, endpoint='convert', params=params)

        if _value:
            return _value

        return None

    @staticmethod
    def get_info(coin, api_key):
        if api_key is None:
            raise Exception("API Key Missing")

        _info = Helper.process_request(coin, endpoint='info', params={
            'apikey': api_key
        })

        if _info:
            return _info

        return None

    @staticmethod
    def get_supported_coins(api_key):
        if api_key is None:
            raise Exception("API Key Missing")

        _info = Helper.get_info('', api_key=api_key)

        _info.pop('fee_tiers', None)

        _coins = {}

        for ticker, coin_info in _info.items():

            if 'coin' in coin_info.keys():
                _coins[ticker] = coin_info['coin']
            else:
                for token, token_info in coin_info.items():
                    _coins[ticker + '_' + token] = token_info['coin'] + ' (' + ticker.upper() + ')'

        return _coins

    @staticmethod
    def get_estimate(coin, addresses=1, priority='default', api_key=''):
        if api_key is None:
            raise Exception("API Key Missing")

        params = {
            'addresses': addresses,
            'priority': priority,
            'apikey': api_key
        }

        _estimate = Helper.process_request(coin, endpoint='estimate', params=params)

        if _estimate:
            return _estimate

        return None

    @staticmethod
    def process_request(coin='', endpoint='', params=None):
        if coin != '':
            coin += '/'

        response = requests.get(
            url="{base_url}{coin}{endpoint}/".format(
                base_url=Helper.BLOCKBEE_URL,
                coin=coin.replace('_', '/'),
                endpoint=endpoint,
            ),
            params=params,
            headers={'Host': Helper.BLOCKBEE_HOST},
        )

        return response.json()
