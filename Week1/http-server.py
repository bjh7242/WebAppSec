#!/usr/bin/env python
# Script to act as a minimal functioning web server
# Requirements:
# -serve an HTML page 
# -should respond to GET POST OPTIONS HEAD and TRACE 
# -should not use any existing library - should use socket 
# -can serve whatever html I want (just one page) 
# -return 404 if it is not a page that is found 
# -implement cookies if it sees a cookie header 
# -if it doesn't get a cookie, it should respond with a set-cookie 
# -print a variable that it gets

import socket
import re
import string
import sys
import random

HOST = ""			# listen on all interfaces
PORT = 8081			# port to listen on

def serve_data(cookie,data,request_type):
    """
    serve_data takes a cookie and a data value (from a POST or GET request) and serves it to a client
    """
    headers = """HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
#COOKIE
"""
    body = """<html>
<head>
<title>SPARSA</title>
</head>
<body>
#DATA
</body>
</html>
"""
    print "METHOD IS " + request_type
    # if cookie does not exist, add one; else don't add cookie header
    if cookie is None:
        cookie = "Set-Cookie: cookie_monster=" + set_cookie()
        headers = string.replace(headers,"#COOKIE",cookie + "\n")
    else:
        temp = string.replace(headers,"#COOKIE","")
        headers = string.replace(temp,"\n\n<html>","\n<html>")

    # set the value to be printed out from the data parameter
    bodytemp = string.replace(body,"#DATA",data)

    # if HEAD request, don't print the body
    if request_type == "HEAD":
        resp = headers
    else:
        resp = headers + bodytemp
    return resp

def receive_request():
    response = "" 

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST,PORT))
        s.listen(1)			# listen with 1 queued connection
    except socket.error as msg:
        s.close()
        s = None
        print msg
        sys.exit()

    while True:
        try:
            conn, addr = s.accept()
            print "Connection from address: " + str(addr)
    
            req = conn.recv(1024)
            if not req:
                break
            print req

            # get_cookie returns None if there is no value for a cookie
            cookie = get_cookie(req)
            req_method = get_method(req)

            # re.search returns None if no match
            if req_method == "GET":
                # extract the value of the data parameter passed in a GET request
                data_regex = re.search("\?data=(.*)HTTP",req)
                if data_regex is not None:
                    data = data_regex.group(1)
                    # build response contents
                    response = serve_data(cookie, data,"GET")
            elif req_method == "POST":
                data = ""
                response = serve_data(cookie, data,"POST")
            elif req_method == "HEAD":
                data = ""
                response = serve_data(cookie, data,"HEAD")
            elif req_method == "OPTIONS":
                response = serve_data(cookie, data,"OPTIONS")
            elif req_method == "TRACE":
                print "METHOD IS TRACE"
                response = req
                print response
            elif req_method is None:
                # should return 405 here
                print "req_method is None"
            
            print "about to sendall"
            conn.sendall(response)
            print "done with sendall"
            conn.close()
        except KeyboardInterrupt:
            print "CTRL-C received. Quitting."
            break
            #sys.exit()
    s.close()

def get_method(request):
    req_method = None

    # methods = case insensitive https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
    method_regex = re.search("^(GET|POST|OPTIONS|HEAD|TRACE)",request)
    # create string from regex object
    req_method =  method_regex.group(0)
    return req_method

def get_cookie(request):
    cookie = None
    cookie_regex = re.search("Cookie: (.*)",request)
    if cookie_regex is not None:
        cookie = cookie_regex.group(1)
    #print "Cookie is " + str(cookie)
    return cookie 

def set_cookie():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])

if __name__ == '__main__':
    receive_request()
