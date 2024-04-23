from requests.models import PreparedRequest
from .BlockBeeRequests import BlockBeeRequests as Req


class BlockBeeCheckoutHelper:
    def __init__(self, api_key, parameters=None, bb_params=None):
        if not parameters:
            parameters = {}

        if not bb_params:
            bb_params = {}

        if not api_key:
            raise Exception("API Key Missing")

        self.parameters = parameters
        self.bb_params = bb_params
        self.api_key = api_key

    def payment_request(self, redirect_url, value):
        if self.parameters:
            req = PreparedRequest()
            req.prepare_url(redirect_url, self.parameters)
            redirect_url = req.url

        params = {
            'redirect_url': redirect_url,
            'apikey': self.api_key,
            'value': value,
            **self.bb_params}

        return Req.process_request_get(None, endpoint='checkout/request', params=params)

    @staticmethod
    def payment_logs(token, api_key):
        params = {
            'apikey': api_key,
            'token': token
        }

        return Req.process_request_get(None, endpoint='checkout/logs', params=params)

    def deposit_request(self, notify_url):
        if self.parameters:
            req = PreparedRequest()
            req.prepare_url(notify_url, self.parameters)
            notify_url = req.url

        params = {
            'notify_url': notify_url,
            'apikey': self.api_key,
            **self.bb_params}

        return Req.process_request_get(None, endpoint='deposit/request', params=params)

    @staticmethod
    def deposit_logs(token, api_key):
        params = {
            'apikey': api_key,
            'token': token
        }

        return Req.process_request_get(None, endpoint='deposit/logs', params=params)
