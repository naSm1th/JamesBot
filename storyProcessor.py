#!/usr/bin/env python

###############################################################################
# storyProcessor.py - the Project Gutenberg story formatter                   #
# takes an input file (formatted as a Project Gutenberg public domain story)  #
# and formats it as a file containing one-line tweets of                      #
# no more than 140 characters                                                 #
#                                                                             #
# usage:                                                                      #
#     python storyProcessor.py inFile outFile                                 #
#         inFile: the story formatted as a                                    #
#                 Project Gutenberg public-domain story                       #
#         outFile: the file that will contain the tweets                      #
#                                                                             #
# Copyright (c) 2014 Nathanael A. Smith                                       #
# License: MIT (see http://opensource.org/licenses/MIT)                       #
###############################################################################

# import the necessary libraries
import sys
import re

# breaks the story into tweets
# parameters:
#     storyFile: the file containing the story
# returns: the tweets, delimited by a newline
def getTweets(storyFile):
    # to be used to build the line
    outLine = ""
    # the lines (being paragraphs)
    pLines = ""    
    # the output lines
    tweets = ""
    
    # first, we must take the story and parse it into paragraphs
    # read all the lines from the file
    lines = storyFile.readlines()
    
    # loop for each line
    for line in lines:
        #if the line is blank
        if (line == "\n"):
            if (outLine != ""):
                # write the previous lines to the file
                # this line is a complete paragraph
                pLines += outLine + '\n'
                outLine = ""
        else:
            # the line is not blank
            # add the line to outLine and strip off the \n character
            if (outLine == ""):
                # we are at the beginning of the line
                outLine += line.rstrip('\n')
            else:
                # we need to add a space to the end of the line
                outLine += " " + line.rstrip('\n')
        
    pLines += outLine
    
    # we have now parsed out the story into one-line paragraphs
    # with no blank lines
    # now we must parse out the individual tweets into lines
    # split the string into an array of lines
    for line in str.splitlines(pLines):
        # if the paragraph is already <= 140 characters, then add it
        if (len(line) <= 140):
            tweets += line + "\n"
        else:
            # split the paragraph into tweets and add them to the output string
            for outLine in splitLine(line):
                tweets += outLine + "\n"
    
    return tweets

# break line into tweets using English grammar
# parameters:
#     line: the string to split into tweets
# returns: an array of tweets
def splitLine(line):
    lines = []
    
    #split at all periods, exclamation points, and question marks
    lines = splitAtSentence(line)
    #split at all semicolons and colons as necessary
    lines = splitAtClause(lines)
    #split at all commas as necessary
    lines = splitAtComma(lines)
    #split mid-sentence, inserting ..., only as necessary
    lines = splitMidSentence(lines)
    
    return lines

# splits the tweets up mid-sentence at a word,
# making the first tweet(s) as large as possible
# paramaters:
#     lines: the array of lines to be processed
# returns: an array of processed lines
def splitMidSentence(lines):
    outLines = []
    curLine = ""
    curPos = 0
    
    # loop for each line given
    for line in lines:
        # if the line is too long, break into words by splitting by spaces
        if len(line) > 140:
            for word in re.split(" ", line):
                # if possible, add the word to the end of the current tweet
                if (len(curLine) + len(word)) < 137:
                    curLine += word + " "
                    curPos += len(word) + 1
                # if necessary, finish up the current tweet and start a new one
                else:
                    curLine = curLine[0:len(curLine)-1] + "..."
                    outLines.append(curLine)
                    curLine = word + " "
                    curPos += len(word) + 1
            curPos = 0
            curLine = ""
        else:
            outLines.append(line)
    return outLines

# splits the tweets at commas
# paramaters:
#     lines: the array of lines to be processed
# returns: an array of processed lines
def splitAtComma(lines):
    outLines = []
    lastPos = 0
    
    # loop for each line given
    for line in lines:
        # if the line is too long, break it up
        # by splitting at commas (and any punctuation/whitespace)
        # and add it to the array of lines
        if len(line) > 140:
            for pos in re.finditer("[,]\p*\s*", line):
                outLines.append(line[lastPos:pos.end(0)])
                lastPos = pos.end(0)
            
            if lastPos != len(line):
                outLines.append(line[lastPos:len(line)])
            lastPos = 0
        else:
            outLines.append(line)
    return outLines

# splits the tweets at semicolons and colons
# paramaters:
#     lines: the array of lines to be processed
# returns: an array of processed lines
def splitAtClause(lines):
    outLines = []
    lastPos = 0
    
    # loop for each line given
    for line in lines:
        # if the line is too long, break it up
        # by splitting at colons/semicolons (and any punctuation/whitespace)
        # and add it to the array of lines
        if len(line) > 140:
            for pos in re.finditer("[;:]\p*\s*", line):
                outLines.append(line[lastPos:pos.end(0)])
                lastPos = pos.end(0)
            
            if lastPos != len(line):
                outLines.append(line[lastPos:len(line)])
            lastPos = 0
        else:
            outLines.append(line)
    return outLines

# splits the tweets at semicolons and colons
# paramaters:
#     lines: the array of lines to be processed
# returns: an array of processed lines
def splitAtSentence(line):
    lines = []
    
    lastPos = 0
    
    # break the tweet into sentences
    # splits at periods (ignoring prefixes), exclamation points, and
    # question marks including any punctuation/whitespace that follows
    # and adds the results to the resulting list
    for pos in re.finditer("(?<=(?<!Mr)(?<!Mrs)(?<!Ms)(?<!Dr)(?<!Jr)(?<!St)"
            + "(?!\")(?!\')[.!?][.\"'\s)])\s*", line):
        lines.append(line[lastPos:pos.end(0)])
        lastPos = pos.end(0)
    
    if lastPos != len(line):
        lines.append(line[lastPos:len(line)])
    lastPos = 0
    
    return lines

# the main method for the story processor
def main():
    # first argument: the input file
    inFile = open(sys.argv[1])
    # second argument: the output file
    outFile = open(sys.argv[2], "w")
    # break the story into tweets
    tweets = getTweets(inFile)
    # write the tweets to the output file
    outFile.write(tweets)
    # close the files
    inFile.close()
    outFile.close()

# run main on execution
if __name__ == "__main__":
        main()
