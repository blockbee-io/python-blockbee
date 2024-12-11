"""
Running tests on BlockBee Library

Uncomment the sections you wish to test
"""

from blockbee import BlockBeeHelper, BlockBeeCheckoutHelper

apikey = ''  # <- Insert your API Key here to run the tests

bb = BlockBeeHelper(
    'sol_usdt',
    '',
    'https://webhook.site/15d94bb3-c3ae-4b68-8120-5dd962988a6d',
    {
        'order_id': 13435
    },
    {
        'convert': 1
    }, apikey)

"""
Get BlockBee Address
"""
# print(bb.get_address()['address_in'])

"""
Get coin information
"""
# print(BlockBeeHelper.get_info('btc'))

"""
Get all supported coins
"""
# print(BlockBeeHelper.get_supported_coins())

"""
Get Logs
"""
# print(bb.get_logs())

"""
Get QR Code
"""
# print(bb.get_qrcode()['qr_code'])

"""
Get Conversion
"""
# print(bb.get_conversion('eur', 100))

"""
Get Estimate
"""
# print(bb.get_estimate('ltc', api_key=apikey))

"""
Create Payout
"""
# print(BlockBeeHelper.create_payout(
#     'bep20_usdt',
#     {
#         '0xA6B78B56ee062185E405a1DDDD18cE8fcBC4395d': 0.5,
#         '0x18B211A1Ba5880C7d62C250B6441C2400d588589': 0.1
#     },
#     api_key=apikey,
#     process=False
# ))

"""
List Payouts
"""
# print(BlockBeeHelper.list_payouts('polygon_pol', status='pending', api_key=apikey, payout_request=True))

"""
Get payout wallet
"""
# print(BlockBeeHelper.get_payout_wallet('polygon_pol', api_key=apikey, balance=True))

"""
Create payout by Payout Request IDs
"""
# print(BlockBeeHelper.create_payout_by_ids(api_key=apikey, payout_ids=[
#     'e74475bb-87a1-4935-8cc0-d2a7f0cbce16',
# ]))

"""
Process Payout
"""
# print(BlockBeeHelper.process_payout(api_key=apikey, payout_id="bb1a462c-b78c-4409-93d9-f3b1328903ec"))

"""
Check Payout Status
"""
# print(BlockBeeHelper.check_payout_status(api_key=apikey, payout_id="bb1a462c-b78c-4409-93d9-f3b1328903ec").get('payout_info')['status'])

###

# bb_checkout = BlockBeeCheckoutHelper(api_key=apikey, parameters={
#     'order_id': 1324556
# })

"""
Request payment URL
"""
# print(bb_checkout.payment_request('https://webhook.site/ab8a5cb9-46aa-41d4-909b-3d27117147b3', 1))

"""
Check Checkout Payment logs
"""
# print(BlockBeeCheckoutHelper.payment_logs(token='OcRrZGsKQFGsoi0asqZkr97WbitMxFMb', api_key=apikey))

"""
Request deposit URL
"""
# print(bb_checkout.deposit_request('https://webhook.site/ab8a5cb9-46aa-41d4-909b-3d27117147b3'))

"""
Check Checkout Deposit logs
"""
# print(BlockBeeCheckoutHelper.deposit_logs(token='fRjFeZodME7lR9ackji5Ft5ecX0VCbBq', api_key=apikey))
