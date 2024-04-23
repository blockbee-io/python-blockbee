from .BlockBeeRequests import BlockBeeRequests as Req
from requests.models import PreparedRequest


class BlockBeeHelper:
    BLOCKBEE_URL = 'https://api.blockbee.io/'
    BLOCKBEE_HOST = 'api.blockbee.io'

    def __init__(self, coin, own_address, callback_url, parameters, bb_params, api_key):
        if not parameters:
            parameters = {}

        if not bb_params:
            bb_params = {}

        if not api_key:
            raise Exception("API Key Missing")

        if not callback_url:
            raise Exception("Callback URL is Missing")

        if not coin:
            raise Exception('Coin is Missing')

        self.coin = coin
        self.own_address = own_address
        self.callback_url = callback_url
        self.parameters = parameters
        self.bb_params = bb_params
        self.api_key = api_key
        self.payment_address = ''

    def get_address(self):
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

        _address = Req.process_request_get(coin, endpoint='create', params=params)

        self.payment_address = _address['address_in']

        return _address

    def get_logs(self):
        coin = self.coin
        callback_url = self.callback_url

        if self.parameters:
            req = PreparedRequest()
            req.prepare_url(self.callback_url, self.parameters)
            self.callback_url = req.url

        params = {
            'callback': callback_url,
            'apikey': self.api_key
        }

        return Req.process_request_get(coin, endpoint='logs', params=params)

    def get_qrcode(self, value='', size=300):
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

        return Req.process_request_get(self.coin, endpoint='qrcode', params=params)

    def get_conversion(self, from_coin, value):
        params = {
            'from': from_coin,
            'value': value,
        }

        return Req.process_request_get(self.coin, endpoint='convert', params=params)

    @staticmethod
    def get_info(coin, api_key=''):
        return Req.process_request_get(coin, endpoint='info')

    @staticmethod
    def get_supported_coins(api_key=''):
        _info = BlockBeeHelper.get_info(coin=None)

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
        params = {
            'addresses': addresses,
            'priority': priority
        }

        return Req.process_request_get(coin, endpoint='estimate', params=params)

    @staticmethod
    def create_payout(coin, payout_requests, api_key, process=False):
        body = {'outputs': payout_requests}

        endpoint = 'payout/request/bulk'

        if process:
            endpoint = endpoint + '/process'

        return Req.process_request_post(coin, endpoint, api_key, body, True)

    @staticmethod
    def list_payouts(coin, status='all', page=1, api_key='', payout_request=False):
        params = {
            'apikey': api_key,
            'status': status,
            'p': page
        }

        endpoint = 'payout/list'

        if payout_request:
            endpoint = 'payout/request/list'

        return Req.process_request_get(coin, endpoint, params)

    @staticmethod
    def get_payout_wallet(coin, api_key, balance=False):
        wallet = Req.process_request_get(coin, 'payout/address', {'apikey': api_key})

        output = {'address': wallet.get('address')}

        if balance:
            wallet_balance = Req.process_request_get(coin, 'payout/balance', {'apikey': api_key})

            if wallet_balance.get('status') == 'success':
                output['balance'] = wallet_balance.get('balance')

        return output

    @staticmethod
    def create_payout_by_ids(api_key, payout_ids):
        return Req.process_request_post('', 'payout/create', api_key, {'request_ids': ','.join(map(str, payout_ids))})

    @staticmethod
    def process_payout(api_key, payout_id):
        return Req.process_request_post('', 'payout/process', api_key, {'payout_id': payout_id})

    @staticmethod
    def check_payout_status(api_key, payout_id):
        return Req.process_request_post('', 'payout/status', api_key, {'payout_id': payout_id})
