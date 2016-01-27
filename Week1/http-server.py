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

def serve_data(cookie,data):
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
    # do some stuff here
    serve_data("lolcookie","loldata")

get_request()
