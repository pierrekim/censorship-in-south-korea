#!/usr/bin/python


# CONCEPT
# 
# 1.
# Client ->
# GET http://google.com/ HTTP/1.1
# 
# 2.
# Proxy -> HTTP Server
# HEAD / HTTP/1.1
# Host: hacktheplanet
# GET http://google.com/ HTTP/1.1
#
# 3.
# Proxy -> Client
# Response to (GET http://google.com/ HTTP/1.1)

# Code from http://luugiathuy.com/2011/03/simple-web-proxy-python/

import os,sys,thread,socket

MAX_CONN = 256
MAX_DATA_RECV = 65336

listen_port = 8090
listen_host = '127.0.0.1'

def main():
    print "Starting HEAD-then-GET PoC Proxy Server on", listen_host, ":", listen_port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((listen_host, listen_port))
        s.listen(MAX_CONN)
    
    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message
        sys.exit(1)

    while 1:
        conn, client_addr = s.accept()
        thread.start_new_thread(proxy_thread, (conn, client_addr))
        
    s.close()


def proxy_thread(conn, client_addr):
    request    = conn.recv(MAX_DATA_RECV)
    first_line = request.split('\n')[0]
    url        = first_line.split(' ')[1]

    print "Request to", url
    
    http_pos = url.find("://")
    temp = url[(http_pos + 3):]


    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)

    webserver = temp[:webserver_pos]

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.connect((webserver, 80))
	request = "HEAD / HTTP/1.1\nHost: hacktheplanet\nConnection: Keep-Alive\n\n" + request
        s.send(request)
        
        req = 0
        while 1:
            data = s.recv(MAX_DATA_RECV)
            if (req != 0):
                if (len(data) > 0):
                    conn.send(data)
                else:
                    break
                if not data:
                    break
            req = req + 1
        s.close()
        conn.close()
    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        sys.exit(1)

if __name__ == '__main__':
    main()
