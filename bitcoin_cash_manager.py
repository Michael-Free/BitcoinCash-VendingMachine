"""
Name:
    Bitcoin Cash Manager

Author:
    Michael Free

Version:
    V.1.0

"""
from cashaddress import convert
from bitcash import PrivateKeyTestnet
from bitcash.network import currency_to_satoshi_cached

def calculate_rate(total_coins_accepted):
    """
    Calculate the price of BCH in Satoshis for the Canadian Dollars with a markup.
    """
    dollar_rate = 0.2 # 20%
    calc_margin = total_coins_accepted * dollar_rate
    add_profit = total_coins_accepted - calc_margin
    bch_rate = currency_to_satoshi_cached(add_profit, 'cad')
    return bch_rate


def verify_address(bch_address):
    """
    Verify the Bitcoin Cash address provided and convert the address
    format if an older one was provided.
    """
    if bch_address.startswith('bchtest:') == True:
        try:
            if convert.is_valid(bch_address) == True:
                print('VALID TESTNET ADDRESS!')
                verified_address = bch_address
                return verified_address
        except ValueError:
            return str('None')
    if bch_address.startswith('bchtest:') == False:
        try:
            if convert.is_valid(bch_address) == True:
                print('ADDRESS IS VALID! DOESNT START WITH CASHADDRESS HEADER')
                verified_address = convert.to_cash_address(bch_address)
                return verified_address
        except ValueError:
            return str('None')

def send_crypto(bch_rate, verified_address):
    """
    Send Satoshis to an address provided.
    """
    tx_inputs = [(verified_address, bch_rate, 'satoshi')]
    KEY.address()
    KEY.get_balance()
    send_bch = KEY.send(tx_inputs, fee=0)
    return send_bch
