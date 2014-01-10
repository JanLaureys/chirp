Chirpy
====================

Cuckoo-clock chirping away when something happens on your twitter.

## Electronics

Chirpy is built using a raspberry pi and the 16-channel 12 bit servo board. Right now I need 2 power sources, but I hope to make some kind of power adapter that can power both the raspberry pi and the servo board, because Chirpy will need to be hung from a wall. It wouldn't look good to have 2 power cables running down from it.

This is the basic scheme for the electronics, except I don't use the breakout cable I just plug directly onto the GPIO pins.

http://learn.adafruit.com/system/assets/assets/000/001/720/original/ServoSketch.png?1345136644

## Software

Chirpy runs on python. It uses the Adafruit servo driver and a few python libraries to hook it up to Twitter. 

## Links

__Servo control board__
http://www.adafruit.com/products/815


