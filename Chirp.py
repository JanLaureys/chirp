#!/usr/bin/python

# Settings paths on where to look for modules

import sys
sys.path.append('Adafruit_PWM_Servo_Driver')
sys.path.append('python-twitter-1.1')

# ===========================================================================
# Setting up the base class
# ===========================================================================

class Chirpy(Object):
  user = ""
  last_direct_message = ""
  follower_count = 0
  favourite_count = 0
  staged_retweet = 0
  staged_directmessage = 0
  staged_mention = 0
  staged_follower = 0

chirp = Chirpy()

# ===========================================================================
# Playing an audio file
# ===========================================================================

import pygame
pygame.mixer.init()
pygame.mixer.music.load("test.wav")
pygame.mixer.music.set_volume(1.0)

def chirp_sound():
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
  pwm.setPWM(3,0,servoMin)                # Reset the motor to the initial setting

def chirp_motor():
  pwm.setPWM(3, 0, servoMin)
  time.sleep(0.333)
  pwm.setPWM(3, 0, servoMax)
  time.sleep(0.5)
  pwm.setPWM(3,0, servoMin)

def chirp_stage(type="", count= "1"):
  if(type=="retweet"):
    chirp.staged_retweet = chirp.staged_retweet + count
  if(type=="follower"):
    chirp.staged_follower = chirp.staged_follower + count
  if(type=="mention"):
    chirp.staged_mention = chirp.staged_mention + count
  if(type=="dm"):
    chirp.staged_directmessage = chirp.staged_directmessage + count

def chirp_get_followers():
  newFollowersCount = chirp.user.followers_count - chirp.follower_count
  chirp.follower_count = chirp.user.followers_count

  if(newFollowers > 0):
    chirp_stage('followser', newFollowersCount)

def chirp_get_direct_messages():
  dms = api.GetDirectMessages(since_id = chirp.last_direct_message)
  print "All direct messages since the last one"
  print dms

  for dm in dms:
    chirp_stage('dm', 1)

def chirp_cycle():
  for follower in range(0, chirp.staged_follower):
    chirp_motor()
    sleep(1)

  for dm in range(0, chirp.staged_directmessage):
    chirp_motor()
    sleep(1)

  chirp.staged_follower = 0
  chirp.staged_directmessage = 0

# ===========================================================================
# Tweeting like a baws
# ===========================================================================

import twitter

print "Logging in to twitter"

# Loggin into the api
api = twitter.Api(consumer_key='H09pUgFTtCLw6crCAay7ow', consumer_secret='9fnAtbJafPZHXoFjaBiGJlM73hSW30bpKdaF9HuOw', access_token_key='15678818-dqIsqYhd63E1ZtsL0FtPzWrOhzDjUz5sDQ0G7V5kU', access_token_secret='RQoo0nqHRpPQKoUoNrQtD01pHAy5CPr0mTRk1jor4lvI7')
credentials = api.VerifyCredentials()

# Getting the user object
chirp.user = api.GetUser(credentials.id)
chirp.favourite_count = chirp.user.favourites_count

# Set the initial direct message
dm = api.GetDirectMessages(count=1)
print dm
chirp.last_direct_message = dm.id

def twitter_poll():
  print "Initializing twitter poll"

  chirp.user = api.GetUser(credentials.id)

  chirp_get_followers()
  chirp_get_direct_messages()

  chirp_cycle()


  time.sleep(180)
  twitter_poll()

# Start the poller
twitter_poll()








