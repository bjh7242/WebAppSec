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

HOST = ""			# listen on all interfaces
PORT = 8080			# port to listen on

def serve_data(cookie,data,request_type):
    """
    serve_data takes a cookie and a data value (from a POST or GET request) and serves it to a client
Cookie: #COOKIE
    """
    temp = """HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0

<html>
<head>
<title>SPARSA</title>
</head>
<body>
#DATA
</body>
</html>
"""
    resp = string.replace(temp,"#COOKIE",cookie)
    resp = string.replace(temp,"#DATA",data)
    print resp
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

    conn, addr = s.accept()
    print "Connection from address: " + str(addr)
    req = conn.recv(1024)
    if not req:
        sys.exit()
    print req

    # methods = case insensitive https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
    method_regex = re.search("^(GET|POST|OPTIONS|HEAD|TRACE)",req)
    # create string from regex object
    req_method =  method_regex.group(0)
    print "req_method is " + req_method
    # re.search returns None if no match
    if req_method == "GET":
        # extract the value of the data parameter passed in a GET request
        data_regex = re.search("\?data=(.*)HTTP",req)
        if data_regex is not None:
            data = data_regex.group(1)
            # build response contents
            response = serve_data("lolcookie",data,"GET")
    elif req_method == "POST":
        pass
    elif req_method == "HEAD":
        pass
    elif req_method == "OPTIONS":
        pass
    elif req_method == "TRACE":
        print "METHOD IS TRACE"
        response = req
        print response
    elif req_method is None:
        # should return 405 here
        print "req_method is None"
    
    conn.sendall(response)
    print "Done sending response"
    s.close()
    print "Closing socket"

receive_request()