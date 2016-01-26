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


