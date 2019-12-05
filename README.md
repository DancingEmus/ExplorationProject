# Exploration Project
CP320 Exploration Project - RFID reader with database support\
By: Aayush Sheth: 160642890 & Michael Pintur: 150785070 

## Overview
  We used a Parralax RFID with a sqlite3 database to simulate a room security system. We first start by storing RFID cards into the database either as a user with access or as banned user. When a user who has been added into the database with access scans their card, a bi-color LED will turn green indicating that the user has access. While when a banned user scans their card the LED will flicker red, and a 5v buzzer will go off.  When a user who has not been added to the database tries to scan their card, the LED will turn red alongside the buzzer to indicate that the user cannot enter. 

## Challenges
In terms of hardware the first issue we had was that the pi only has one serial port available on it and because of that we weren't able to use putty to remotely work with the pi. We had to manually set it up with the screen and work directly on it. Next the RFID reader was rather lackluster and would rarely read the cards/tokens right corrrectly the first time. It would often timeout and not read the whole card and in often cases it just wouldn't register the card/token at all. In terms of software errors there were a lot of issues with line endings and indentention because we were copying code over that we wrote on windows to a unix based system. The solution to this was to go through the code line by and address each one of those issues individually.


## Libraries Needed
1.https://docs.python.org/2/library/sqlite3.html
SQLite library was needed for database operations.

2.https://pyserial.readthedocs.io/en/latest/pyserial.html
Serial library was required as the RFID reader ran on serial ports.


## Useful URLS
1. https://www.raspberrypi.org/forums/ 
Link to the raspberry pi forums. It was helpful because it allowed to us find a lot of information on how to integrate our devices with the pi and allowed us to debug issues quicker.

2. http://denethor.wlu.ca/projects/sensors/28140-28340-RFID_Reader-v2.1.pdf
The data sheet for the RFID reader, gave us details on how to wire up the RFID reader.

3. http://denethor.wlu.ca/raspberry_pi/rpi_RFID.shtml
Link to Terry's webpage about the RFID reader. Gives an overview about the device and has examples on how to write code to have it work with the serial interface on the pi.


## Video
[![](https://img.youtube.com/vi/AqpAeMQy2bc&t=16s/0.jpg)](https://www.youtube.com/watch?v=AqpAeMQy2bc&t=16s)
