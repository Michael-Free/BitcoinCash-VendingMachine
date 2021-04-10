# DIY Cryptocurrency Vending Machine

<p align="center">
<img src="/media/gumball_machine.jpg" width="25%" height="25%">
</p>

## DONATE 
qrvyahhjwygm0eurz2rxctln6en26kf07vz0zancl7

## Description
This project serves as a proof-of-concept Cryptocurrency Vending Machine (or "ATM"), more widely known as a "Bitcoin ATM." The aim is to teach people about how Bitcoin, and other cryptocurrencies work.  The idea came about when at a meetup group where people were still new to the space, but wanted to learn about how this works by enabling to buy small amounts of crypto and learn about setting up a wallet, as well as sending and receiving crypto.

This Vending Machine was designed with simplicity in mind from the code all way through using inexpensive off-the-shelf parts like Arduino, Raspberry Pi, and other Hobby Electronics parts. The great thing about this project is that it isn't necesarily tied down to any platform.  This can theoretically can be used on x86 based computers, rather than a Raspberry Pi, but could be used on other Single Board Computers. All it needs to have is the ability to run Python 3.  This gives the flexibility for people to set this up on their own PC or recomission an older one they have around, if they choose to do so.

## Table of Contents
* [Disclaimer](#disclaimer)
* [Hardware Requirements](#hardware-requirements)
* [Software Requirements](#software-requirements)
* [Training A Coin Acceptor](#training-a-coin-acceptor)
* [Arduino Components](#arduino-software-components)
  * [LCD Panel with Arduino](#lcd-panel-with-arduino)
  * [Coin Acceptor with Arduino](#coin-acceptor-with-arduino)
* [Arduino Flashing](#arduino-flashing)
* [Arduino Wiring](#arduino-wiring)
* [Setting Up Twilio](#setting-up-twilio)
* [Setting up ngrok](#setting-up-ngrok)
* [Wallet Management](#wallet-management)
  * [Creating a Bitcoin Cash Wallet](#creating-a-bitcoin-cash-wallet)
  * [Getting Testnet Bitcoin Cash](#getting-testnet-bitcoin-cash)
* [Configuration File](#configuration-file)
* [Python Components](#python-components)
  * [Coin Acceptor](#coin-acceptor)
  * [Bitcoin Cash Manager](#bitcoin-cash-manager)
  * [Kiosk Server](#kiosk-server)
* Running the Vending Machine
  * Create new Testnet Bitcoin Cash Address
  * Starting the Server

## Disclaimer
Please note that this repository hasn't been through a security audit, and running anything in a production scenario would be considered "unwise."  Before running this in any scenario please realise that this is incubent on the end user to understand and apply legislation in the jurisdictions they are operating this hardware/software in and to be in compliance with their local authorities.

## Hardware Requirements
- 1 x Raspberry Pi 3 - https://amzn.to/3aYAC9X
- 1 x SD Card - https://amzn.to/38QM9Wd
- 1 x USB Power Supply - https://amzn.to/2X2Yf9a
- 2 x Arduino Uno - https://amzn.to/2KIFLZh
- 1 x LCD Panel Sheild - https://amzn.to/38RbRd5
- 1 x Coin Acceptor - https://amzn.to/3rKQR0j
- 1 x 10k Ohm Resistor - https://amzn.to/38RbRd5
- 3 x Dupont Cables - https://amzn.to/38QMIPP
- 2 x USB type B to USB type A - https://amzn.to/3o7P5Ee
- 1 x Universal Power Adaptor - https://amzn.to/2X3Jbs6

## Software Requirements
Most of the requirements are default libraries in Python.  Aside from them, the following are requirements:
* Ubuntu 18.04+ OR Rasbpian OS Buster+
  * Either can be installed on the Raspberry Pi 3b+ but Ubuntu 18.04 would be needed if this is going to be installed on a PC.
* Python 3.7+ plus these libraries:
  * configparser - needed to interpret the contents of `config.ini`
  * serial - needed for serial communication between the computer and the arduinos
  * flask - web application framework for communication with the end user, twilio, and more
  * twilio - library needed to interact with twilio's API.  Twilio interfaces with the end user via text message.
  * cashaddress - this converts a legacy Bitcoin Cash Address to the new address format.
  * bitcash - a bitcoin cash library for python.
* Arduino Software IDE 1.8+
  * This doesn't need to be installed on the ATM Pi/PC. 
  * It only needs to be used on the computer you're using to write to the Arduino itself.

## Training a Coin Acceptor
Here is a copy of the manual that's freely available online, but I have included it here in this documentation.  This is a great way to learn about the acceptor and have it trained for every type of coin you might throw at it:
<p align="center">
<img src="/media/ch-926-instructions.jpg">
</p>
This animation is directly from Adafruit's documentation and purchase page. This animation show's it's for the CH-924, but it's identical for the CH-926. The only difference between the two is that the CH-924 takes 4 different types of coins, while the CH-926 takes 6.
<p align="center">
<img src="/media/coin-programming.gif">
</p>
While this explanation can go much deeper, my intent is not to re-invent the wheel. Guides that can teach you this is done by a little bit of Google-Fu.

## Arduino Software Components
There are going to be two different scripts that we're going to have to write to each of our two Arduinos.  

One script is going to control the LCD Panel connected to an Arudino.  This Arduino will be connected to the computer via a USB Serial Connection.  The computer is going to control what is going to be written to the LCD Panel with the Serial Connection. The calls to write to this LCD Panel is going to be controlled directly by the [Kiosk Server](#kiosk-server).

The other script is going to deal with reading what coins are dropped into the coin acceptor and emitting an electrical pulse. The electric pulses are counted, and read with a dollar value.  That dollar value is then transmitted via a second USB Serial Connection on the main computer.  Then `arduino_coin_acceptor.py` receives that information over a period of time, and then adds up the dollar value of everything and passes that on the `bitcoin_cash_manager.py` to calculate exchange rates of the dollar value deposited.

### LCD Panel with Arduino

<p align="center">
<img src="/media/lcd_screen.png" width="25%" height="25%">
</p>

This is a fairly common 16x2 character LCD shield for Arduino, that's made by many numbers of different manufacturers for relatively cheap.  This will be hooked up to an Arduino that will communicate via serial port, and will also receive commands via serial port to display text on-the-fly as commands are sent through the `kiosk_server.py` program.  `write_to_lcd_from_serial.ino` is not written by myself, it is widely available and created by Mark Bramwell all the way back in 2010.

### Coin Acceptor with Arduino
The sensors in this coin acceptor use the thickness, diameter and fall time of the coins to identify them and it's fully programmable so you're not limited to any particular type of currency. Simply use the buttons and 7-segment display on the side of the unit to select a coin profile, insert a bunch of coin samples and you're good to go! After you've programmed the coin profiles, the coin acceptor will recognize them and report when each type is inserted, rejecting other coins.  The output is reported by a number of electrical pulses that are linked to each type of coin programmed.

These electrical pulses will be received by an arduino (with `coin_acceptor.ino`) - and interpreted by `coin_acceptor_arduino.py`. `coin_acceptor.ino` currently is setup to read $2, $1, 25¢, and 10¢ Canadian coins.  Each coin gives off a certain number of pulses:

```
switch (newCoinInserted) {
  case 3:   
    Serial.println("2");
    newCoinInserted = 0;   
    break;
  case 6:   
    Serial.println("1");
    newCoinInserted = 0;   
    break;
  case 9:   
    Serial.println("0.25");
    newCoinInserted = 0;   
    break;
  case 12:   
    Serial.println("0.10");
    newCoinInserted = 0;   
    break;
```
The timing may have to be adjusted to get the most accurate readings from the coin acceptor.  When the coins are dropped in, it will communicate this information over serial port to the computer/raspberry pi.

## Arduino Flashing
1. To program the Arduino board you need the Arduino environment. Download Arduino from arduino.cc
2. Connect the first board
3. The power LED should go on.
4. Upload each program
5. Push the reset button on the board then click the Upload button in the IDE. Wait a few seconds. If successful, the message "Done uploading." will appear in the status bar.

## Arduino Wiring
This is a quick diagram of how the coin acceptor is wired up directly to one of the Arduinos. If you you hold the coin acceptor upside-right the order in which the wires appear will appear in the correct order.  This is what  it will look like when you face the Arduino, facing up, with the USB port pointing to the right.
<p align="center">
<img src="/media/arduino_coinacceptor.png" width="75%" height="75%">
</p>

## Setting up Twilio
Twilio allows software developers to programmatically make and receive phone calls, send and receive text messages, and perform other communication functions using its web service APIs.

1. Create Free/Paid Account: www.twilio.com/referral/Dm61NZ
2. Create a DID phone number: https://www.twilio.com/docs/phone-numbers
3. Create API Access Tokens: https://www.twilio.com/docs/iam/access-tokens

## Setting up ngrok
ngrok is a tool that creates a secure tunnel on your local machine along with a public URL you can use for browsing your local site. This will be used to help us communicate with the Twilio service to initiate and finish transaction.s When ngrok is running, it listens on the same port that you're local web server is running on and proxies external requests to your local machine.  You will need to sign up for a free account to use ngrok.

1. Unzip ngrok from a terminal with the following command.
```
unzip /path/to/ngrok.zip
```
2. In the ngrok settings, you will be able to get your authorization token.  Running this command will add your authtoken to your ngrok.yml file. Connecting an account will list your open tunnels in the dashboard, give you longer tunnel timeouts, and more. Visit the dashboard to get your auth token.
```
./ngrok authtoken <your_auth_token>
```
3. Start an HTTP tunnel on port 5000, run this next:
Read the documentation to get more ideas on how to use ngrok.
```
./ngrok http 5000
```

https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment#install-ngrok

## Wallet Management

### Creating a Bitcoin Cash Wallet

Before getting some Testnet Bitcoin Cash, we'll need to get ourselves a mobile wallet.  The first Testnet Wallet will be a mobile one.  The easiest way to set one up is with BitPay's wallet.  We'll be using this one because it's available on Android and iOS.  It's also easily setup through their support pages:

* https://bitpay.com/wallet/
* https://support.bitpay.com/hc/en-us/articles/360015463612-How-to-Create-a-Testnet-Wallet

Now that we have the mobile wallet setup to receive Test BCH, we'll need to set up the wallet that will be on the ATM.  To start, we'll need to fire up a python 3 console by typing `python3` into the Linux terminal.

```
>>> from bitcash import PrivateKeyTestnet
>>> key = PrivateKeyTestnet()
```
The first thing we'll do once we're in the Python3 import the libraries needed to create a new address.  Then we will define the `key` variable.
```
>>> key.address
'bchtest:qq24s5vinyj1g7nfgm8fvj346ad7hcujjd4ck8kdg7'
```
The next thing we'll do is call the `address()` property to get the public BCH test address.  Once this is entered, you'll see some output as above, giving you the Bitcoin Cash address. Save this address somewhere, because we'll need it when we go to get some Testnet BCH.

```
>>> key.to_wif()
'xSAkj43tAk9k2Sk1Ak4JAtR1sakiSODqdkrAkWsQ9A9K7ALEA8kW'
```
The next thing we'll need for this address is to get the private key for the address we just created. This will be needed when we create transactions to be sent from the ATM to your mobile wallet. This private key will be needed as well when we setup our `config.ini` file.

### Getting Testnet Bitcoin Cash

Since this hasn't been made to work on mainnet, it's using testnet Bitcoin Cash. You could get yourself some testnet BCH through various methods like mining - however, the quickest way would be through a faucet that gives you some free testnet BCH for testing your applications!  Check out some of these great links to get started:

* https://developer.bitcoin.com/faucet/
* https://faucet.fullstack.cash/
* https://testnet-faucet.electroncash.de/
* https://testnet.help/en

When you're asked for your addres, make sure you put in your address that was created when you entered `key.address` in the previous step.

## Configuration File
The configuration file, `config.ini` has been setup to make this easy for everyone to get up and running with this repository. It's divided up into 3 different sections that require some configuration and your input.

```
[TWILIO]
account_sid = <account_sid>
auth_token = <auth_token>
```
The first section is for connecting and interacting with Twilio's API.  This will require the Account SID and the API authentication token. If there's any issues in finding this information, this guide is quite helpful: https://www.comm100.com/livechat/knowledgebase/where-do-i-find-the-twilio-account-sid-auth-token-and-phone-number-sid.html

```
[CONNECTIONS]
lcd_panel = /dev/ttyACM0
coin_acceptor = /dev/ttyUSB0
```
Under this section, the serial communication between the two Arduinos and the Flask server.  Typically on a Raspberry Pi, the Arduino can look like `/dev/ttyACM`.  If this is going to be running on a x86-based computer, the Arduino can be found under `/dev/ttyUSB`.  If you're having trouble locating them, take a look under your Arduino IDE and they'll be found there when you flash the devices. 

If this is being ran in a headless state and there's no access to a GUI and the Arduino IDE - the Arduino's can be found by using `dmesg`. If you're still having trouble finding it, you can unplug and plug back in the Arduino while running `dmesg | tail -f` - and it should show the correct port.

```
[CRYPTOWALLET]
wallet_address = <address_here>
wallet_privkey = <private_key>
```
With the CryptoWallet section - this is where you'll be setting up the information regarding the wallet, so when they machine is used, it can interact with the blockchain. The address we created in the python command prompt (and the private key) can be put here.

## Python Components
Please make sure to review the description and code of each component for this project. The only component that is actualy "ran" is the Kiosk Server and the other two components' functions are merely imported into it to be used.

The reason these are not included as part of the Kiosk Server component is to be able to test these components outside of the kiosk server it self, to speed up development, as well as to provide support for multiple different coins in the future.

### Coin Acceptor
`coin_acceptor_arduino.py` is the python interface between the Arduino that's wired to the coin acceptor.  It's main functions is to receive input from each coin inserted via serial port for a period of time (in seconds).  After it accepts each coin, it then tallies up the amount of coins accepted over that period of time. From there, this information can be processed by `bitcoin_cash_manager.py` to calculate the exchange rate and send the Bitcoin Cash to the proper address.

### Bitcoin Cash Manager
`bitcoin_cash_manager.py` contains the 3 core functions needed to make transactions work correctly with the kiosk server. The main functions are:
- calculate the current exchange rate from BCH to CAD
- verify that the address submitted is correct (so that the transcation can be sucessful)
- send BCH from the local wallet to the submitted BCH address

### Kiosk Server
`kiosk_server.py` is the main component that runs, which inherits functions directly from `coin_acceptor.py` and `bitcoin_cash_manager.py`. It uses serial communication to show information on the Arduino LCD panel, and handles the text message communication via Twilio's APIs all on a simple Flask webserver.

## Running the Vending Machine

### Getting It All Setup

It's time to connect everything together. Pretty sure this is straight-forward for most people to follow.

<p align="center">
<img src="/media/diagram.png" width="75%" height="75%">
</p>


### Starting the Server

** FYI This is still a work in progress and documentation is still being completed **


