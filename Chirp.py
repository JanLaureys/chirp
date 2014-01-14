#!/usr/bin/python

# Settings paths on where to look for modules

import sys
sys.path.append('Adafruit_PWM_Servo_Driver')
sys.path.append('python-twitter-1.1')

# ===========================================================================
# Tweeting like a baws
# ===========================================================================

import twitter

api = twitter.Api(consumer_key='H09pUgFTtCLw6crCAay7ow',
                      consumer_secret='9fnAtbJafPZHXoFjaBiGJlM73hSW30bpKdaF9HuOw',
                      access_token_key='15678818-dqIsqYhd63E1ZtsL0FtPzWrOhzDjUz5sDQ0G7V5kU',
                      access_token_secret='RQoo0nqHRpPQKoUoNrQtD01pHAy5CPr0mTRk1jor4lvI7')

credentials = api.VerifyCredentials()

print "Welcome " % credentials.name



# ===========================================================================
# Playing an audio file
# ===========================================================================

import pygame
pygame.mixer.init()
pygame.mixer.music.load("test.wav")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()

# ===========================================================================
# Controlling the servo
# ===========================================================================

from Adafruit_PWM_Servo_Driver import PWM
import time

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)

servoMin = 165  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
#
#while (True):
  # Change speed of continuous servo on channel
#  pwm.setPWM(3, 0, servoMin)
#  time.sleep(0.333)
#  pwm.setPWM(3, 0, servoMax)
#  time.sleep(0.333)



