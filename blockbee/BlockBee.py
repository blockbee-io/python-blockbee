"""
BlockBee's Python Helper
"""

import requests
import json
from requests.models import PreparedRequest

from urllib.parse import urljoin, urlencode


class BlockBeeHelper:
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

        _address = BlockBeeHelper.process_request_get(coin, endpoint='create', params=params)
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

        _logs = BlockBeeHelper.process_request_get(coin, endpoint='logs', params=params)

        if _logs:
            return _logs

        return None

    def get_qrcode(self, value='', size=300):
        if self.coin is None:
            return None

        address = self.payment_address

        if not address:
            address = self.get_address().get('address_in')

        params = {
            'address': address,
            'size': size,
            'apikey': self.api_key
        }

        if value:
            params['value'] = value

        _qrcode = BlockBeeHelper.process_request_get(self.coin, endpoint='qrcode', params=params)

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

        _value = BlockBeeHelper.process_request_get(self.coin, endpoint='convert', params=params)

        if _value:
            return _value

        return None

    @staticmethod
    def get_info(coin, api_key):
        if api_key is None:
            raise Exception("API Key Missing")

        _info = BlockBeeHelper.process_request_get(coin, endpoint='info', params={
            'apikey': api_key
        })

        if _info:
            return _info

        return None

    @staticmethod
    def get_supported_coins(api_key):
        if api_key is None:
            raise Exception("API Key Missing")

        _info = BlockBeeHelper.get_info('', api_key=api_key)

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

        _estimate = BlockBeeHelper.process_request_get(coin, endpoint='estimate', params=params)

        if _estimate:
            return _estimate

        return None

    @staticmethod
    def create_payout(coin, payout_requests, api_key, process=False):
        if not payout_requests:
            raise ValueError('No requests provided')

        body = {'outputs': payout_requests}

        endpoint = 'payout/request/bulk'

        if process:
            endpoint = endpoint + '/process'

        _payout = BlockBeeHelper.process_request_post(coin, endpoint, api_key, body, True)

        if _payout.get('status') == 'success':
            return _payout

        return None

    @staticmethod
    def list_payouts(coin, status = 'all', page = 1, api_key = '', payout_request=False):
        if not api_key:
            return None

        params = {
            'apikey': api_key,
            'status': status,
            'p': page
        }

        endpoint = 'payout/list'

        if payout_request:
            endpoint = 'payout/request/list'

        _payouts = BlockBeeHelper.process_request_get(coin, endpoint, params)

        if _payouts.get('status') == 'success':
            return _payouts

        return None

    @staticmethod
    def get_payout_wallet(coin, api_key, balance=False):
        wallet = BlockBeeHelper.process_request_get(coin, 'payout/address', {'apikey': api_key})

        if wallet.get('status') != 'success':
            return None

        output = {'address': wallet.get('address')}

        if balance:
            wallet_balance = BlockBeeHelper.process_request_get(coin, 'payout/balance', {'apikey': api_key})

            if wallet_balance.get('status') == 'success':
                output['balance'] = wallet_balance.get('balance')

        return output

    @staticmethod
    def create_payout_by_ids(api_key, payout_ids):
        if not payout_ids:
            raise ValueError('Please provide the Payout Request(s) ID(s)')

        _payout = BlockBeeHelper.process_request_post('', 'payout/create', api_key, {'request_ids': ','.join(map(str, payout_ids))})

        if _payout.get('status') == 'success':
            return _payout

        return None

    @staticmethod
    def process_payout(api_key, payout_id):
        if not payout_id:
            return None

        _process = BlockBeeHelper.process_request_post('', 'payout/process', api_key, {'payout_id': payout_id})

        if _process.get('status') == 'success':
            return _process

        return None

    @staticmethod
    def check_payout_status(api_key, payout_id):
        if not id:
            raise ValueError('Please provide the Payout ID')

        _status = BlockBeeHelper.process_request_post('', 'payout/status', api_key, {'payout_id': payout_id})

        if _status.get('status') == 'success':
            return _status

        return None

    @staticmethod
    def process_request_get(coin='', endpoint='', params=None):
        if coin != '':
            coin += '/'

        response = requests.get(
            url="{base_url}{coin}{endpoint}/".format(
                base_url=BlockBeeHelper.BLOCKBEE_URL,
                coin=coin.replace('_', '/'),
                endpoint=endpoint,
            ),
            params=params,
            headers={'Host': BlockBeeHelper.BLOCKBEE_HOST},
        )

        return response.json()

    @staticmethod
    def process_request_post(coin='', endpoint='', apiKey='', body=None, isJson=False):
        if coin:
            coin_path = coin.replace('_', '/') + '/'
        else:
            coin_path = ''

        url = urljoin(BlockBeeHelper.BLOCKBEE_URL, f"{coin_path}{endpoint}/")
        url += '?' + urlencode({'apikey': apiKey})

        headers = {
            'Host': BlockBeeHelper.BLOCKBEE_HOST,
        }

        if isJson:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(body)
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            data = urlencode(body)

        response = requests.post(url, headers=headers, data=data)

        return response.json()
