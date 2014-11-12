#!/usr/bin/env python

###############################################################################
# James.py - the main TwitterBot file                                         #
# uses the Twython library and an Arduino over USB serial to send tweets      #
# from files specified in a settings file                                     #
#                                                                             #
# Copyright (c) 2014 Nathanael A. Smith                                       #
# License: MIT (see http://opensource.org/licenses/MIT)                       #
###############################################################################

# import the necessary libraries
import sys
import serial
from twython import Twython

# the various private keys used to access the Twitter account
# these keys are obtained by creating a new Twitter App and approving access
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

# the serial settings for Arduino
# the Arduino serial port
ARDUINO_PORT = "/dev/ttyACM0"
# the baud rate
ARDUINO_BAUD = 9600

# the settings filename
SETTINGS_FILE = "settings.txt"

# retrieves a tweet using the story and position specified in the settings file
def getTweet():
    # open the settings file with read/write permissions
    settingsFile = open(SETTINGS_FILE, "r+")
    
    # read the first line, omitting the newline character
    # this is the story filename
    fileName = settingsFile.readline().replace("\n", "");
    # get the current position in the settings file
    # we will use this later to update the position recorded here
    position = settingsFile.tell()
    # read the story's current position
    tweetPosition = settingsFile.readline()
    
    # open the story file
    tweetFile = open(fileName)
    # go to the story's current position as read from the settings file
    tweetFile.seek(int(tweetPosition))
    
    # read a line (previously formatted as one tweet)
    tweet = tweetFile.readline()

    # set the current story position
    settingsFile.truncate(position)
    settingsFile.seek(position)
    position = str(tweetFile.tell())
    if position=="":
        position=0;
    settingsFile.write(position)
    
    # for debugging: print the tweet to stdout
    print tweet
    # return the tweet
    return tweet.replace("\n", "")

# posts a line to Twitter using the specified API
# paramaters:
#    api: the previously-initialized Twython object with which to post
def postLine(api):
	tweet=getTweet()
	if tweet!="":
		api.update_status(status=tweet)
	
# the main method for the TwitterBot
def main():
    # create a new Twython object using the appropriate keys
    api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
    # open the Arduino's serial port
    arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD)
    
    # loop infinitely
    while(1):
        # if the arduino says the door is open, send a tweet
        if arduino.read()=='1':
            postLine(api)
        
    # we are done; close the port
    arduino.close()


# run main on execution
if __name__ == "__main__":
    main()
