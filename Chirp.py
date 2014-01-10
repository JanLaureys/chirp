#!/usr/bin/python

# Settings paths on where to look for modules

import sys
sys.path.append('Adafruit_PWM_Servo_Driver')

# ===========================================================================
# Playing an audio file
# ===========================================================================

import pygame
pygame.mixer.init()
pygame.mixer.music.load("test.wav")
pygame.mixer.music.set_volume(1)
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
while (True):
  # Change speed of continuous servo on channel
  pwm.setPWM(3, 0, servoMin)
  time.sleep(0.333)
  pwm.setPWM(3, 0, servoMax)
  time.sleep(0.333)



