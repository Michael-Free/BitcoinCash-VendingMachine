"""
Name:
    Bitcoin Cash DIY Vending Machine

Author:
    Michael Free

Version:
    V.1.0 

"""
import configparser
#from  import Serial
from flask import Flask, request
from bitcoin_cash_manager import send_crypto, verify_address, calculate_rate
from coin_acceptor_arduino import count_coins, add_coins
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
CONFIG = configparser.RawConfigParser()
CONFIG.read('config.ini')

KEY = CONFIG['CRYPTOWALLET']['wallet_privkey']
COIN_ACCEPTOR = CONFIG['CONNECTIONS']['coin_acceptor']
#COIN_TIME = CONFIG['']['']
APP = Flask(__name__)
BOOTSTRAP = Bootstrap(APP)
APP.config['SECRET_KEY'] = 'TempSecretKey'

def start_session():
    """
    Start a new session to drop in coins and receive cryptocurrency.
    """
    started_session = start_session.has_been_called == True
    return started_session

start_session.has_been_called = False

def start_transaction(message_body):
    """
    Receive a message and verify it is a valid address, start the coin
    acceptor, count coins being dropped, calculate the rate, and send
    the cryptocurrency.
    """
    if verify_address(message_body) != 'None':
        print('Address verfified! ' + message_body + ' Insert Coins for 10 seconds')
        print('INSERT COINS')
        money_added = add_coins(count_coins(COIN_ACCEPTOR, 10))
        print(b'Total = $' + str(money_added))
        sent_crypto = send_crypto(calculate_rate(money_added), message_body)
        start_session.has_been_called = False
    if verify_address(message_body) == 'None':
        sent_crypto = print('Address not valid!')
        start_session.has_been_called = False
    return sent_crypto

@APP.route('/', methods=['GET', 'POST'])
def home():
    """
    """
    return render_template('home.html')
    
@APP.route("/buybch", methods=['GET'])
def buybch():
    """
    """

    return render_template('buybch.html')

@APP.route("/receipt", methods=['POST'])
def receipt():
    """
    """
    return render_template('receipt.html')

if __name__ == '__main__':
    APP.run()
