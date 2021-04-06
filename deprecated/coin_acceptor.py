"""
# @author    Robert Souliere
# @version   1.0
#
# Prototyping an online ATM-type interface for purchasing Crypto.
# Designed to work with an actual physical coin-acceptor device to accept cash payment.
# Subsequently process a purchase transaction of the selected Crypto device/coin.
# The physical coin-acceptor can be replaced by an online emulation process as demonstrated below.
#
"""
import time
import datetime
from datetime import timedelta
import traceback
# import raspberry pi GPIO module.
import RPi.GPIO as GPIO
print('Program Start: >' + str(datetime.datetime.now()) + '<')

# GPIOZero module became available with Python 3, and can easily be used in
# place of the older RPi.GPIO
#import GPIOzero

# the following emulator is a useful substitute for simple GPIO testing, without the
# need for a physical device.  GPIO function support is limited and does not
# currently include support for the add_event_detect function.
# Further information about this emulator can be found at the following link:
# roderickvella.wordpress.com/2016/06/28/raspberry-pi-gpio-emulator/
# from EmulatorGui import GPIO

print('Program: >' + ' Set GPIO mode and pins ' + '<')
# http://pinout.xyz
GPIO.setmode(GPIO.BCM)
COIN_ACCEPTOR_SIGNAL_PIN = 18
GPIO.setup(COIN_ACCEPTOR_SIGNAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#==> Explore: This way of initializing a Python array is evil:
#   a=[[]]*2; a[0].append('foo'); now inspect a[1],
#   and you will be shocked. In contrast a=[[] for k in range(2)] works fine. – Joachim W
#==>
EVENT = []
EVENTS = []
#==>
COINS = [0, 0, 0, 0, 0, 0]
#==>
PULSE_COUNT = 0
PULSE_WIDTH = 50
INTER_PULSE_WIDTH = 100
TOLERANCE = 0.10
PULSE_WIDTH_UPPER = PULSE_WIDTH + (PULSE_WIDTH * TOLERANCE)
PULSE_WIDTH_LOWER = PULSE_WIDTH - (PULSE_WIDTH * TOLERANCE)
INTER_PULSE_WIDTH_UPPER = INTER_PULSE_WIDTH + (INTER_PULSE_WIDTH * TOLERANCE)
INTER_PULSE_WIDTH_LOWER = INTER_PULSE_WIDTH - (INTER_PULSE_WIDTH * TOLERANCE)
#==>
PREVIOUS_EVENT_TIMESTAMP = datetime.datetime.now()

def my_callback(channel):
    """
    my callback
    """
    current_event_timestamp = datetime.datetime.now()
    #EVENT = []
    EVENT.append(current_event_timestamp)
    EVENT.append(channel)
    EVENT.append(GPIO.input(channel))
    EVENTS.append(EVENT)
    print('EVENT:' + str(len(EVENTS)))
#    print('event:' + str(len(EVENTS)) + str(EVENTS))
#    current_event = float(EVENT_TIMESTAMP[-8:])
#    print(float(str(datetime.datetime.now())[-8:]))
#    if GPIO.input(channel) == GPIO.HIGH:
try:
    # setup pin 23 as an input.  Pin 23 is a parallel circuit to pin 18, and is being used to
    # monitor the output of pin 18.  These 2 pins should behave in an identical manner -
    # High when High / Low when Low.
    # A Raspberry Pi internal Pull-UP resistor is used, since the closed circuit is
    # connected to Ground.
    # A Pull-DOWN resistor would be used for a closed circuit connected to Source.
    # The following link is a good start for information about the use of pull_up and pull_down
    # resistors, why they are needed and using the internal Raspberry Pi equivalents.
    # https://grantwinney.com/using-pullup-and-pulldown-resistors-on-the-raspberry-pi/
    #

    print('Program: >' + ' Start GPIO event detection ' + '<')
    GPIO.add_event_detect(COIN_ACCEPTOR_SIGNAL_PIN, GPIO.BOTH, callback=my_callback)
#    message = input('\nPress any key to exit.\n')

except Exception as ex:
    traceback.print_exc()

while True:
    time.sleep(0.2)
    if len(EVENTS) > 0:
        EVENT = EVENTS.pop(0)
        EVENT_TIMESTAMP = EVENT[0]
        EVENT_CHANNEL = EVENT[1]
        EVENT_LEVEL = EVENT[2]
        print('Process event ...')
        print(EVENT_TIMESTAMP)
        print(EVENT_CHANNEL)
        print(EVENT_LEVEL)
        EVENT_TIME_DELTA = EVENT_TIMESTAMP - PREVIOUS_EVENT_TIMESTAMP
        EVENT_TIME_DELTA_MILLISECONDS = (EVENT_TIME_DELTA / timedelta(milliseconds=1))
        print(EVENT_TIME_DELTA)
        print(EVENT_TIME_DELTA_MILLISECONDS)
        if EVENT_LEVEL and EVENT_TIME_DELTA_MILLISECONDS > INTER_PULSE_WIDTH_UPPER:
            print('\nNew coin at: ' + str(EVENT_TIMESTAMP))
            if PULSE_COUNT:
                if not PULSE_COUNT % 3:
                    COINS[int(PULSE_COUNT / 3)] += 1
                    print('COINS:' + str(COINS))
            PULSE_COUNT = 0
        elif EVENT_LEVEL and EVENT_TIME_DELTA_MILLISECONDS < INTER_PULSE_WIDTH_LOWER:
            print('\nHigh signal out of range!! (previous)>' + str(PREVIOUS_EVENT_TIMESTAMP))
            print('\nHigh signal out of range!!  (current)>' + str(EVENT_TIMESTAMP))
        elif EVENT_LEVEL:
            pass
        elif not EVENT_LEVEL and PULSE_WIDTH_LOWER < EVENT_TIME_DELTA_MILLISECONDS < PULSE_WIDTH_UPPER:
            PULSE_COUNT += 1
            print('pulse count: ' + str(PULSE_COUNT))
        elif not EVENT_LEVEL:
            print('\nLow signal out of range!! (previous)>' + str(PREVIOUS_EVENT_TIMESTAMP))
            print('\nLow signal out of range!!  (current)>' + str(EVENT_TIMESTAMP))

        if len(EVENTS) == 0 and PULSE_COUNT:
            if not PULSE_COUNT % 3:
                COINS[int(PULSE_COUNT / 3)] += 1
                print('COINS:' + str(COINS))
                PULSE_COUNT = 0
        PREVIOUS_EVENT_TIMESTAMP = EVENT_TIMESTAMP
        print('out:' + str(EVENT_TIMESTAMP))
        print('out:' + str(EVENT_CHANNEL))
        print('out:' + str(EVENT_LEVEL))
    else:
        pass
#exit()

print('Program Stop: >' + str(datetime.datetime.now()) + '<')
