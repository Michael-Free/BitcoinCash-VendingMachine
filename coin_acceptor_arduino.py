"""
Name:
    Arduino Coin Acceptor Interface

Author:
    Michael Free

Version:
    V.1.0

"""
import time
from decimal import Decimal
from serial import Serial

def count_coins(serial_device, time_period):
    """
    Receive the value of each input from the Arduino to the serial port
    for a period of seconds.
    """
    coin_acceptor = Serial(serial_device, baudrate=9600)
    coin_accepted = []
    wait_time = time.time() + int(time_period) * 1
    while time.time() < wait_time:
        readline = coin_acceptor.readline()
        coin_accepted.append(str(readline.decode('utf-8')).rstrip('\n').rstrip('\r'))
    return coin_accepted

def add_coins(coin_accepted):
    """
    From all the input received, parse the data and add up each value.
    """
    coin_accepted.remove('Initialized...')
    coin_accepted = [Decimal(coins) for coins in coin_accepted]
    coin_accepted = ["{:.2f}".format(coins) for coins in coin_accepted]
    coin_accepted = [float(coins) for coins in coin_accepted]
    total_coin_accepted = round(sum(coin_accepted), 2)
    coin_accepted.clear()
    return total_coin_accepted

