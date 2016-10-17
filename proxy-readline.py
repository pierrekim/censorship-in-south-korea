#!/usr/bin/python


# CONCEPT
# 
# 1.
# Client ->
# GET http://google.com/ HTTP/1.1
# 
# 2.
# Proxy -> HTTP Server
# request is sent line by line to the remote server
#
# 3.
# Proxy -> Client

# Code from http://luugiathuy.com/2011/03/simple-web-proxy-python/

import os,sys,thread,socket

MAX_CONN = 256
MAX_DATA_RECV = 65336

listen_port = 8083
listen_host = '127.0.0.1'

def main():
    print "Starting Line-by-Line PoC Proxy Server on", listen_host, ":", listen_port
    print "Works using KT"

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

        for req in request.split('\n'):
            s.send(req + '\n')
        
        while 1:
            data = s.recv(MAX_DATA_RECV)
            if (len(data) > 0):
                conn.send(data)
            else:
                break
            if not data:
                break
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
