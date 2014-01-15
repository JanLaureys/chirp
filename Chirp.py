#!/usr/bin/python

# Settings paths on where to look for modules

import sys
sys.path.append('Adafruit_PWM_Servo_Driver')
sys.path.append('python-twitter-1.1')

# ===========================================================================
# Load configuration
# ===========================================================================

config = {}
execfile("chirp.conf", config)

# ===========================================================================
# Setting up the base class
# ===========================================================================

class Chirpy(object):
  user = ""
  last_direct_message = ""
  last_mention = ""
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
  print "Chirp_stage"
  if(type=="retweet"):
    chirp.staged_retweet = chirp.staged_retweet + count
  if(type=="follower"):
    chirp.staged_follower = chirp.staged_follower + count
  if(type=="mention"):
    chirp.staged_mention = chirp.staged_mention + count
  if(type=="dm"):
    chirp.staged_directmessage = chirp.staged_directmessage + count

def chirp_get_followers():
  print "chirp_get_followers"
  newFollowersCount = chirp.user.followers_count - chirp.follower_count
  chirp.follower_count = chirp.user.followers_count

  if(newFollowersCount > 0):
    chirp_stage('followser', newFollowersCount)

def chirp_get_direct_messages():
  print "chirp_get_direct_messages"
  dms = api.GetDirectMessages(since_id = chirp.last_direct_message)

  reset = 0 

  for dm in dms:
    if(reset==0):
      chirp.last_direct_message = dm.id
      reset = 1 
    chirp_stage('dm', 1)

def chirp_get_mentions():
  print "chirp_get_mentions"
  mentions = api.GetMentions(since_id = chirp.last_mention)

  reset = 0 

  for mention in mentions:
    if(reset==0):
      chirp.last_direct_message = mention.id
      reset = 1 
    print mention.text
    chirp_stage('mention', 1)

def chirp_cycle():
  print "chirp_cycle"
  for follower in range(0, chirp.staged_follower):
    chirp_motor()
    time.sleep(1)

  for dm in range(0, chirp.staged_directmessage):

    chirp_motor()
    time.sleep(1)

  chirp.staged_follower = 0
  chirp.staged_directmessage = 0

# ===========================================================================
# Initializing
# ===========================================================================

print "Testing engines"
chirp_motor()
chirp_motor()

import twitter

print "Logging in to twitter"

# Loggin into the api
api = twitter.Api(consumer_key=config["consumer_key"], consumer_secret=config["consumer_secret"], access_token_key=config["access_token_key"], access_token_secret=config["access_token_secret"])
credentials = api.VerifyCredentials()

# Getting the user object
chirp.user = api.GetUser(credentials.id)
chirp.favourite_count = chirp.user.favourites_count

# Set the initial direct message
lastdm = api.GetDirectMessages(count=1)

for dm in lastdm:
  chirp.last_direct_message = dm.id

# Set the initial mention
lastmention = api.GetMentions(count=1)

for lm in lastmention:
  chirp.last_mention = lm.id

def twitter_poll():
  print "Polling twitter for the latest date"

  # Reload the user object
  chirp.user = api.GetUser(credentials.id)

  # Get things from the user
  chirp_get_followers()
  chirp_get_direct_messages()
  chirp_get_mentions()

  chirp_cycle()

  print "Going to sleep for a minute"
  print "=================================================================="

  time.sleep(60)
  twitter_poll()

# Start the poller
twitter_poll()








