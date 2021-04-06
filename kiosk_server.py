"""
Name:
    Bitcoin Cash DIY Vending Machine

Author:
    Michael Free

Version:
    V.1.0 

"""
import configparser
from serial import Serial
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from bitcoin_cash_manager import send_crypto, verify_address, calculate_rate
from coin_acceptor_arduino import count_coins, add_coins

CONFIG = configparser.RawConfigParser()
CONFIG.read('config.ini')

KEY = CONFIG['CRYPTOWALLET']['wallet_privkey']
LCD_PANEL = Serial(CONFIG['CONNECTIONS']['lcd_panel'], baudrate=9600)
COIN_ACCEPTOR = CONFIG['CONNECTIONS']['coin_acceptor']
COIN_TIME = CONFIG['']['']
ACCOUNT_SID = CONFIG['TWILIO']['account_sid']
AUTH_TOKEN = CONFIG['TWILIO']['auth_token']
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
RESP = MessagingResponse()

APP = Flask(__name__)
LCD_PANEL.setDTR(False)

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
        RESP.message('Address verfified! ' + message_body + ' Insert Coins for 10 seconds')
        LCD_PANEL.write(b'INSERT COINS')
        money_added = add_coins(count_coins(COIN_ACCEPTOR, 10))
        LCD_PANEL.write(b'Total = $' + str(money_added))
        sent_crypto = send_crypto(calculate_rate(money_added), message_body)
        start_session.has_been_called = False
    if verify_address(message_body) == 'None':
        sent_crypto = LCD_PANEL.write(b'Address not valid!')
        start_session.has_been_called = False
    return sent_crypto

@APP.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    """
    Receive or Send a Twilio text message depending on what input has been received.
    """
    number = request.form['From']
    message_body = request.form['Body']
    begin_statement = 'BEGIN'
    if message_body == begin_statement:
        if start_session.has_been_called == False:
            start_session()
            RESP.message('{} Your number is on the screen. Text us a BCH address'.format(number))
            text_reply = LCD_PANEL.write(str(number).encode('utf-8'))
        if start_session.has_been_called == True:
            text_reply = LCD_PANEL.write(b'Session Existing!')
    if message_body != begin_statement:
        if start_session.has_been_called == True:
            text_reply = start_transaction(message_body)
        if start_session.has_been_called == False:
            text_reply = LCD_PANEL.write(b'Session Existing!')
    return text_reply
if __name__ == '__main__':
    APP.run()
