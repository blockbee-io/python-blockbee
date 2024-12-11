[<img src="https://blockbee.io/static/assets/images/blockbee_logo_nospaces.png" width="300"/>](image.png)

# BlockBee's Python Library
Python implementation of BlockBee's payment gateway

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [API and utils](#api-and-utils)
4. [Checkout](#checkout)
5. [Payouts](#payouts)
6. [Help](#help)
7. [Changelog](#changelog)

## Requirements:

```
Python >= 3.0
Requests >= 2.20
```

## Installation

```shell script
pip install python-blockbee
```

[on pypi](https://pypi.python.org/pypi/python-blockbee)
or
[on GitHub](https://github.com/blockbee-io/python-blockbee)

## API and utils

### Importing in your project file

```python
from blockbee import BlockBeeHelper
```

### Generating a new Address

```python
from blockbee import BlockBeeHelper

bb = BlockBeeHelper(coin, own_address, callback_url, parameters, bb_params, api_key)

address = bb.get_address()['address_in']
```

#### Where:

* ``coin`` is the coin you wish to use, from BlockBee's supported currencies (e.g 'btc', 'eth', 'erc20_usdt', ...).
* ``own_address`` is your own crypto address, where your funds will be sent to.
* ``callback_url`` is the URL that will be called upon payment.
* ``params`` is any parameter you wish to send to identify the payment, such as `{orderId: 1234}`.
* ``bb_params`` parameters that will be passed to BlockBee _(check which extra parameters are available here: https://docs.blockbee.io/#operation/create).
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).
* ``address`` is the newly generated address, that you will show your users in order to receive payments.

#### Response sample: 

```
0x0E945b1554c8029A6B9bE1F7A24ae75d2F44d8DB
```

### Getting notified when the user pays

> Once your customer makes a payment, BlockBee will send a callback to your `callbackUrl`. This callback information is by default in ``GET`` but you can se it to ``POST`` by setting ``post: 1`` in ``blockbeeParams``. The parameters sent by BlockBee in this callback can be consulted here: https://docs.blockbee.io/#operation/confirmedcallbackget

### Checking the logs of a request

```python

from blockbee import BlockBeeHelper

bb = BlockBeeHelper(coin, own_address, callback_url, parameters, bb_params, api_key)

data = bb.get_logs()
```
> Same parameters as before, the ```data``` returned can b e checked here: https://docs.blockbee.io/#operation/logs

#### Response sample: 

```json
{
  "status": "success",
  "callback_url": "https://example.com/?order_id=1235",
  "address_in": "0x58e90D31530A5566dA97e34205730323873eb88B",
  "address_out": "0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d",
  "notify_pending": false,
  "notify_confirmations": 1,
  "priority": "default",
  "callbacks": []
}
```

### Generating a QR code

```python
from blockbee import BlockBeeHelper

bb = BlockBeeHelper(coin, own_address, callback_url, parameters, bb_params, api_key)

qr_code = bb.get_qrcode(value, size)
```
For object creation, same parameters as before. You must first call ``getAddress` as this method requires the payment address to have been created.

#### Where:

* ``value`` is the value requested to the user in the coin to which the request was done. **Optional**, can be empty if you don't wish to add the value to the QR Code.
* ``size`` Size of the QR Code image in pixels. Optional, leave empty to use the default size of 512.

> Response is an object with `qr_code` (base64 encoded image data) and `payment_uri` (the value encoded in the QR), see https://docs.blockbee.io/#operation/qrcode for more information.

#### Response sample:
```json
{
  "status": "success",
  "qr_code": "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",
  "payment_uri": "0x0E945b1554c8029A6B9bE1F7A24ae75d2F44d8DB"
}
```

#### Usage
```
<img src={`data:image/png;base64,{{qr_code}}`}/>
```

### Estimating transaction fees

```python
from blockbee import BlockBeeHelper

fees = BlockBeeHelper.get_estimate(coin, addresses, priority)
```

#### Where: 
* ``coin`` is the coin you wish to check, from BlockBee's supported currencies (e.g 'btc', 'eth', 'erc20_usdt', ...)
* ``addresses`` The number of addresses to forward the funds to. Optional, defaults to 1.
* ``priority`` Confirmation priority, (check [this](https://support.blockbee.io/article/how-the-priority-parameter-works) article to learn more about it). Optional, defaults to ``default``.

> Response is an object with ``estimated_cost`` and ``estimated_cost_usd``, see https://docs.blockbee.io/#operation/estimate for more information.

#### Response sample:

```json
{
  "status": "success",
  "estimated_cost": "0.00637010",
  "estimated_cost_currency": {
    "AED": "0.03",
    "AUD": "0.01",
    "BGN": "0.01",
    "BRL": "0.04"
  }
}
```

### Converting between coins and fiat

```python
from blockbee import BlockBeeHelper

bb = BlockBeeHelper(coin, own_address, callback_url, params, bb_params, api_key)

conversion = bb.get_conversion(value, from_coin)
```

#### Where:

* ``coin`` the target currency to convert to, from BlockBee's supported currencies (e.g 'btc', 'eth', 'erc20_usdt', ...)
* ``value`` value to convert in `from`.
* ``from_coin`` currency to convert from, FIAT or crypto.

> Response is an object with ``value_coin`` and ``exchange_rate``, see https://docs.blockbee.io/#operation/convert for more information.

#### Response sample:

```json
{ 
  "status": "success", 
  "value_coin": "241.126", 
  "exchange_rate": "0.803753"
}
```

### Getting supported coins

```python
from blockbee import BlockBeeHelper

supportedCoins = BlockBeeHelper.get_supported_coins()
```

> Response is an array with all supported coins.

#### Response sample:

```json
{
  "btc": {
    "coin": "Bitcoin",
    "logo": "https://api.cryptapi.io/media/token_logos/btc.png",
    "ticker": "btc",
    "minimum_transaction": 8000,
    "minimum_transaction_coin": "0.00008000",
    "minimum_fee": 546,
    "minimum_fee_coin": "0.00000546",
    "fee_percent": "1.000",
    "network_fee_estimation": "0.00002518"
  },
  "bch": {
    "coin": "Bitcoin Cash",
    "logo": "https://api.cryptapi.io/media/token_logos/bch.png",
    "ticker": "bch",
    "minimum_transaction": 50000,
    "minimum_transaction_coin": "0.00050000",
    "minimum_fee": 546,
    "minimum_fee_coin": "0.00000546",
    "fee_percent": "1.000",
    "network_fee_estimation": "0.00000305"
  }
}
```

## Checkout

### Requesting Payment

```python
from BlockBee import BlockBeeCheckoutHelper

bb = BlockBeeCheckoutHelper(api_key, params, bb_params)

payment_page = bb.payment_request(redirect_url, value)
```

#### Where:
* ``api_key`` is the API Key provided by our [Dashboard](https://dash.blockbee.io/).
* ``params`` is any parameter you wish to send to identify the payment, such as `{'order_id': 1234}`.
* ``bb_params`` parameters that will be passed to BlockBee _(check which extra parameters are available here: https://docs.blockbee.io/#operation/create).
* ``redirect_url`` URL in your platform, where the user will be redirected to following the payment. Should be able to process the payment using the `success_token`.
* ``value`` amount in currency set in Payment Settings you want to receive from the user.

#### Getting notified when the user completes the Payment
> When receiving payments, you have the option to receive them in either the ``notify_url`` or the ``redirect_url``, but adding the ``redirect_url``  is required (refer to our documentation at https://docs.blockbee.io/#operation/paymentipn).

#### Payment samples:
```json
{
  "status": "success",
  "success_token": "G4asA2xwEr0UeY2IZqlZjX3IYrNofmnIAkzHPAoxmpmlYP9ZLTvQUolKN0X27Z0B",
  "payment_url": "https://pay.blockbee.io/payment/OcRrZGsKQFGsoi0asqZkr97WbitMxFMb/",
  "payment_id": "OcRrZGsKQFGsoi0asqZkr97WbitMxFMb"
}
```

### Payment Logs

Fetch Payment information and IPN logs.

```python
from BlockBee import BlockBeeCheckoutHelper

logs = BlockBeeCheckoutHelper.payment_logs(token, api_key)
```

#### Where:

* ```token``` is the  `payment_id` returned by the payment creation endpoint.
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).

#### Response sample:

```json
{
  "status": "success",
  "is_paid": false,
  "is_pending": false,
  "is_expired": false,
  "is_partial": false,
  "payment_data": [
    {
      "value": "0.000137",
      "value_paid": "0",
      "value_outstanding": "0.000137",
      "exchange_rate": "0.0000137489",
      "coin": "btc",
      "txid": []
    }
  ],
  "notifications": []
}
```

### Requesting Deposit
```python
from BlockBee import BlockBeeCheckoutHelper

bb = BlockBeeCheckoutHelper(api_key, params, bb_params)

deposit_page = bb.deposit_request(notify_url)
```

#### Where:
* ``api_key`` is the API Key provided by our [Dashboard](https://dash.blockbee.io/).
* ``params`` is any parameter you wish to send to identify the payment, such as `{'order_id': 1234}`.
* ``bb_params`` parameters that will be passed to BlockBee (check which extra parameters are available here: https://docs.blockbee.io/#operation/deposit).
* ``notify_url`` URL in your platform, where the IPN will be sent notifying that a deposit was done. Parameters are available here: https://docs.blockbee.io/#operation/depositipn.

#### Response sample:
```json
{
  "status": "success",
  "payment_url": "https://pay.blockbee.io/deposit/jv12du8IWqS96WVDjZK2J285WOBOBycc/",
  "payment_id": "jv12du8IWqS96WVDjZK2J285WOBOBycc"
}
```

### Deposit Logs

Fetch Deposit information and IPN logs.

```python
from BlockBee import BlockBeeCheckoutHelper

logs = BlockBeeCheckoutHelper.deposit_logs(token, api_key)
```

#### Where:

* ```token``` is the  `payment_id` returned by the deposit creation endpoint.
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).

#### Response sample:

```json
{
  "status": "success",
  "deposits": [],
  "total_deposited": "0",
  "currency": "USDT",
  "notifications": []
}
```

## Payouts

### Create Payout / Payout Request

This function can be used by you to create [Payouts](https://docs.blockbee.io/#tag/Payouts).

```python
from BlockBee import BlockBeeHelper

coin = 'polygon_matic'

requests = {
    '0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d': 0.5,
    '0x18B211A1Ba5880C7d62C250B6441C2400d588589': 0.1
}

create_payout = BlockBeeHelper.create_payout(coin, payout_requests, api_key, process)
```

#### Where:
* ``coin`` The cryptocurrency you want to request the Payout in (e.g `btc`, `eth`, `erc20_usdt`, ...).
* ``requests`` Address(es) together with the amount that must be sent.
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).
* ``process`` If the Payout Requests will be sent right away. Defaults to `False`. **Note**: if `True` will instantly queue the payouts to be sent to the destination addresses.

#### Response sample:

If `process` is `false`.
```json
{
  "status": "success",
  "request_ids": [
    "42d5245e-0a29-402a-9a7e-355e38f1d81d",
    "080a546e-4045-4c73-870c-4d9ec08c9cab"
  ]
}
```

If `process` is `true`.
```json
{
  "status": "success",
  "payout_info": {
    "id": "88e5eacc-d5a5-4b8a-8133-e23136151b7c",
    "status": "Pending Payment",
    "from": "0x18B211A1Ba5880C7d62C250B6441C2400d588589",
    "requests": {
      "0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d": "0.5",
      "0x18B211A1Ba5880C7d62C250B6441C2400d588589": "0.1"
    },
    "total_requested": "0.6",
    "total_with_fee": "0.603",
    "error": "None",
    "blockchain_fee": 0,
    "fee": "0.003",
    "coin": "bep20_usdt",
    "txid": "",
    "timestamp": "23/04/2024 11:13:49"
  },
  "queued": true
}
```

### List Payouts / Payout Requests

List all Payouts or Payout Requests in your account.

**Note:** If `requests` is `True` it will fetch a Payout Requests list.

```python
from BlockBee import BlockBeeHelper

create_payout = BlockBeeHelper.list_payouts(coin, status, page, api_key, payout_request)
```

#### Where:
* ``coin`` The cryptocurrency you want to request the lists in (e.g `btc`, `eth`, `erc20_usdt`, ...).
* ``status`` The status of the Payout / Payout Request. Possible statuses are:
    * Payout Request: [`all`, `pending`, `rejected`, `processing`, `done`]
    * Payout: [`created`, `processing`, `done`, `error`]
* ``page`` This endpoint is paginated and will show only `50` items per page. Defaults to `1`.
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).
* ``payout_request`` If `True` will fetch Payout Requests, otherwise will fetch Payouts. Defaults to `False`.

#### Response sample:

```json
{
  "status": "success",
  "payouts": [
    {
      "id": "88e5eacc-d5a5-4b8a-8133-e23136151b7c",
      "status": "Done",
      "total_requested": "0.6",
      "total_with_fee": "0.606",
      "total_fiat": "",
      "fee": "0.006",
      "coin": "polygon_matic",
      "timestamp": "13/03/2024 17:48:39"
    }
  ],
  "num_pages": 1
}
```

### Get Payout Wallet

Gets your Payout Wallet for the specified `coin`. Can algo get the balance.

```python
from BlockBee import BlockBeeHelper

wallet = BlockBeeHelper.get_payout_wallet(coin, api_key, balance)
```

#### Where:
* ``coin`` The cryptocurrency you want to request the lists in (e.g `btc`, `eth`, `erc20_usdt`, ...).
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).
* ``balance`` If `True` will also fetch the balance of the address.

#### Response sample:
```json
{
  "address": "0x18B211A1Ba5880C7d62C250B6441C2400d588589",
  "balance": "2.7"
}
```

### Create Payout with Payout Request ID(s)

With this function you can create a Payout in the `created` status by simply providing an array with the Payout Requests `ID`.

```python
from BlockBee import BlockBeeHelper

ids = [52211, 52212]

payout = BlockBeeHelper.create_payout_by_ids(api_key, payout_ids)
```

#### Where:
* ``payout_ids`` its an array with the Payout Requests `ID`.

#### Response sample:

```json
{
  "status": "success",
  "payout_info": {
    "id": "88e5eacc-d5a5-4b8a-8133-e23136151b7c",
    "status": "Created",
    "from": "",
    "requests": {
      "0xA8EbeD50f2e05fB4a25b2DdCdc651A7CA769B5CF": "0.300000000000000000",
      "0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d": "0.200000000000000000"
    },
    "total_requested": "0.5",
    "total_with_fee": "0.505",
    "total_fiat": "",
    "fee": "0.005",
    "coin": "bep20_usdt",
    "txid": "",
    "timestamp": "05/03/2024 15:00:00"
  }
}
```

### Process Payout by ID

By default, a Payout when created will be in `created` state. With this function you may finish it using its `ID`.

```python
from BlockBee import BlockBeeHelper

payout = BlockBeeHelper.process_payout(api_key, payout_id)
```

#### Where:

* ``payout_id`` Its the `ID` of the Payout you wish to fulfill.

#### Response sample:

```json
{ 
  "status": "success", 
  "queued": true
}
```

### Check the Payout status

Will return all important information regarding a Payout, specially its status.

```python
from BlockBee import BlockBeeHelper

payout_id = 51621

status = BlockBeeHelper.check_payout_status(api_key, payout_id)
```

#### Where:

* ``payout_id`` Its the `ID` of the Payout you wish to check.

#### Response sample:

```json
{
  "status": "success",
  "payout_info": {
    "id": "88e5eacc-d5a5-4b8a-8133-e23136151b7c",
    "status": "Done",
    "from": "0x18B211A1Ba5880C7d62C250B6441C2400d588589",
    "requests": {
      "0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d": "0.500000000000000000",
      "0x18B211A1Ba5880C7d62C250B6441C2400d588589": "0.100000000000000000"
    },
    "total_requested": "0.6",
    "total_with_fee": "0.606",
    "total_fiat": "",
    "fee": "0.006",
    "coin": "polygon_matic",
    "txid": "0xf9aa1618a7e460f8c68b6a02369b5058282c53a4ee23f967abef0d35203f328c",
    "timestamp": "13/03/2024 18:10:35"
  }
}
```

## Help

Need help?  
Contact us @ https://blockbee.io/contacts/


## Changelog

#### 1.0.0
* Initial Release

#### 1.0.1
* Minor fixes

#### 1.0.2
* Minor fixes

#### 1.0.3
* Fix import
* Minor fixes

#### 1.1.0
* Added Payouts
* Minor bugfixes

#### 1.1.1
* Minor bugfixes

#### 2.0.0
* Automated Payouts
* Support to BlockBee Checkout page
* Various improvements

#### 2.0.1
* Minor bugfixes

#### 2.1.0
* Minor bugfixes
* Improve error handling

#### 2.1.1
* Minor improvements

### Breaking Changes

#### 2.0.0
* `create_payout` parameters were changed and will require you to update your code.