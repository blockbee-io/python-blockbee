import BlockBee

apikey = ''  # <- Insert your API Key here to run the tests

bb = BlockBee.Helper('bep20_usdt', '',
                     'https://webhook.site/15d94bb3-c3ae-4b68-8120-5dd962988a6d', {
                         'order_id': 13435
                     }, {
                        'convert': 1
                     }, apikey)

"""
Get BlockBee Address
"""
print('get_address:')
address = bb.get_address()['address_in']
print(address)

"""
Get coin information
"""
print('get_info:')
print(BlockBee.Helper.get_info('btc', api_key=apikey))

"""
Get all supported coins
"""
print('get_supported_coins:')
print(BlockBee.Helper.get_supported_coins(api_key=apikey))

"""
Get Logs
"""
print('get_logs')
print(bb.get_logs())

"""
Get QR Code
"""
print('Get QR Code')
print(bb.get_qrcode()['qr_code'])

"""
Get Conversion
"""
print('Get Conversion')
print(bb.get_conversion('eur', 100, api_key=apikey))

"""
Get Estimate
"""
print('Get Estimate')
print(bb.get_estimate('ltc', api_key=apikey))
