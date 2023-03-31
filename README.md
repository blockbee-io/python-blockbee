[<img src="https://blockbee.io/static/assets/images/blockbee_logo_nospaces.png" width="300"/>](image.png)


# BlockBee's Python Library
Python implementation of BlockBee's payment gateway

## Requirements:

```
Python >= 3.0
Requests >= 2.20
```

## Install

```shell script
pip install python-blockbee
```

[on pypi](https://pypi.python.org/pypi/python-blockbee)
or
[on GitHub](https://github.com/blockbee-io/python-blockbee)

## Usage

### Importing in your project file

```python
from blockbee import BlockBeeHelper
```

### Generating a new Address

```python
from blockbee import BlockBeeHelper

bb = BlockBeeHelper(coin, own_address, callback_url, params, bb_params, api_key)

address = bb.getAddress()['address_in']
```

Where:

* ``coin`` is the coin you wish to use, from BlockBee's supported currencies (e.g 'btc', 'eth', 'erc20_usdt', ...).
* ``own_address`` is your own crypto address, where your funds will be sent to.
* ``callback_url`` is the URL that will be called upon payment.
* ``params`` is any parameter you wish to send to identify the payment, such as `{orderId: 1234}`.
* ``bb_params`` parameters that will be passed to BlockBee _(check which extra parameters are available here: https://docs.blockbee.io/#operation/create).
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).
* ``address`` is the newly generated address, that you will show your users in order to receive payments.

### Getting notified when the user pays

> Once your customer makes a payment, BlockBee will send a callback to your `callbackUrl`. This callback information is by default in ``GET`` but you can se it to ``POST`` by setting ``post: 1`` in ``blockbeeParams``. The parameters sent by BlockBee in this callback can be consulted here: https://docs.blockbee.io/#operation/confirmedcallbackget

### Checking the logs of a request

```python

from blockbee import BlockBeeHelper

bb = BlockBeeHelper(coin, own_address, callback_url, params, bb_params, api_key)

data = bb.get_logs()
```
> Same parameters as before, the ```data``` returned can b e checked here: https://docs.blockbee.io/#operation/logs

### Generating a QR code

```python
from blockbee import BlockBeeHelper

bb = BlockBeeHelper(coin, own_address, callback_url, params, bb_params, api_key)

###

qr_code = bb.get_qrcode(value, size)
```
For object creation, same parameters as before. You must first call ``getAddress` as this method requires the payment address to have been created.

For QR Code generation:

* ``value`` is the value requested to the user in the coin to which the request was done. **Optional**, can be empty if you don't wish to add the value to the QR Code.
* ``size`` Size of the QR Code image in pixels. Optional, leave empty to use the default size of 512.

> Response is an object with `qr_code` (base64 encoded image data) and `payment_uri` (the value encoded in the QR), see https://docs.blockbee.io/#operation/qrcode for more information.

### Estimating transaction fees

```python
from blockbee import BlockBeeHelper

fees = BlockBeeHelper.get_estimate(coin, addresses, priority, api_key)
```
Where: 
* ``coin`` is the coin you wish to check, from BlockBee's supported currencies (e.g 'btc', 'eth', 'erc20_usdt', ...)
* ``addresses`` The number of addresses to forward the funds to. Optional, defaults to 1.
* ``priority`` Confirmation priority, (check [this](https://support.blockbee.io/article/how-the-priority-parameter-works) article to learn more about it). Optional, defaults to ``default``.
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).

> Response is an object with ``estimated_cost`` and ``estimated_cost_usd``, see https://docs.blockbee.io/#operation/estimate for more information.

### Converting between coins and fiat

```python
from blockbee import BlockBeeHelper

conversion = BlockBeeHelper.get_conversion(value, from_coin, api_key)
```
Where:
* ``coin`` the target currency to convert to, from BlockBee's supported currencies (e.g 'btc', 'eth', 'erc20_usdt', ...)
* ``value`` value to convert in `from`.
* ``from_coin`` currency to convert from, FIAT or crypto.
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).

> Response is an object with ``value_coin`` and ``exchange_rate``, see https://docs.blockbee.io/#operation/convert for more information.

### Getting supported coins

```python
from blockbee import BlockBeeHelper

supportedCoins = BlockBeeHelper.get_supported_coins(api_key)
```
Where: 
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).

> Response is an array with all supported coins.

### Request Payout

```python
from blockbee import BlockBeeHelper

payout = BlockBeeHelper.create_payout(coin, address, value, apiKey)
```

This function can be used by you to request payouts (withdrawals in your platform).

Where:
* ``coin`` The cryptocurrency you want to request the Payout in (e.g `btc`, `eth`, `erc20_usdt`, ...).
* ``address`` Address where the Payout must be sent to.
* ``value`` Amount to send to the ``address``.
* ``api_key`` is the API Key provided by BlockBee's [dashboard](https://dash.blockbee.io/).

> The response will be only a ``success`` to confirm the Payout Request was successfully created. To fulfill it you will need to go to BlockBee Dashboard.


## Help

Need help?  
Contact us @ https://blockbee.io/contacts/


### Changelog

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