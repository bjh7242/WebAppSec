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

HOST = ""			# listen on all interfaces
PORT = 8080			# port to listen on

def serve_data(cookie,data,request_type):
    """
    serve_data takes a cookie and a data value (from a POST or GET request) and serves it to a client
    """
    temp = """HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Cookie: #COOKIE

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

def get_request():
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(1)			# listen with 1 queued connection
    conn, addr = s.accept()
    print "Connection from address: " + str(addr)
    while True:
        req = conn.recv(1024)
        if not req:
            break
        print req

        # methods = case insensitive https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
        method = re.search("^(GET|POST|OPTIONS|HEAD|TRACE)",req)
        print method.group(0)
        # re.search returns None if no match
        if method is None:
            # should return 405 here
            pass
        print str(method)

    serve_data("lolcookie","loldata","GET")

get_request()
