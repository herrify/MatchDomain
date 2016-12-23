#!/usr/bin/env python3

'''
created: 2016-11-30 10:04:18
@author: johnny
'''

import requests
import re
import json
from datetime import datetime, timezone, timedelta
import time
import random
import threading

__data__ = {}   # Warning: Dont Modify This Line! 

class v2ex:
    def __init__(self, username='', password=''):
        if username and password:
            self.u = username
            self.p = password
        else:
            self.u = input("Username: ")
            self.p = input("Password: ")

        self.signout = True
        self.s = requests.session()

    def __del__(self): self.s.close()

    def login(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Origin': 'https://www.v2ex.com',
            'Referer': 'https://www.v2ex.com/signin',
            'Host': 'www.v2ex.com'
        }
        content = self.s.get('https://www.v2ex.com/signin').text
        once = re.findall(r'value="(\d+)" name="once"', content)[0]
        u, p = re.findall(r'class="sl" name="(.+)" value', content)

        payload = {
            u: self.u,
            p: self.p,
            'next': '/',
            'once': once
        }
        self.signout = self.s.post('https://www.v2ex.com/signin', data=payload, headers=headers).text.find('signout') == -1
        return self.signout

    def sign(self):
        if self.signout:
            print(self.u, 'login failed!')
            return
        if self.content:
            try:
                with open(__file__, "w") as f:
                    f.write(self.content)
            except:
                print("File", __file__, "write failed!")

        '''
        <div class="sep20"></div>
        <div class="box">
            <div class="inner"><li class="fa fa-gift" style="color: #f90;"></li> &nbsp;<a href="/mission/daily">领取今日的登录奖励</a></div>
        </div>

        '''
        if self.s.get('http://www.v2ex.com/').text.find('领取今日的登录奖励') == -1:
            print(self.u, 'has been signed in.')
            return

        try:
            daily = re.findall(r'(/mission/daily/redeem\?once=\d+)', self.s.get("http://www.v2ex.com/mission/daily").text)[0]
            self.s.get('http://www.v2ex.com'+daily, headers={"Referer": "http://www.v2ex.com/mission/daily"})
            print(self.u, 'Sign-in Success.')
        except:
            print(self.u, 'Dont Sign-in Again!')

    def again(self):
        today = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%dUTC+8')
        if len(__data__) != 1 or today not in __data__:
            try:
                with open(__file__, "r") as f:
                    self.content = re.sub(r'([\n\r]+__data__\s*=\s*){.*?}', r'\1%s' % json.dumps({today: [self.u]}), f.read())
            except:
                print("File", __file__, "read failed!")
            __data__[today] = [self.u]
            return False

        if self.u not in __data__.get(today, []):
            __data__[today].append(self.u)
            try:
                with open(__file__, "r") as f:
                    self.content = re.sub(r'([\n\r]+__data__\s*=\s*){.*?}', r'\1%s' % json.dumps(__data__), f.read())
            except:
                print("File", __file__, "read failed!")
            return False
        self.content = None
        return True

    def daily(self):
        if self.again():
            print(self.u, 'Dont Sign-in Again!')
            return
        self.login()
        self.sign()

class CronWork:
    def __init__(self, fn=None):
        self.cron_times = []
        self.cron_run = True
        self.cron_fn = fn
        self.cron_thread = threading.Thread(target=self.CronLoop)

    def Run(self):
        self.cron_thread.start()
        self.CommandLoop()

    def SleepTime(self):
            yield 1
            while self.cron_run:
                if len(self.cron_times) > 2:
                    self.cron_times.pop(0)
                elif len(self.cron_times) == 0:
                    self.cron_times.append(5)
                    self.cron_times.append(10)
                elif len(self.cron_times) == 1:
                    self.cron_times.append(10)
                else: pass
                left, right = self.cron_times[0:2]
                if left > right: left, right = right, left
                yield random.randint(left, right)

    def CronLoop(self):
            for num in self.SleepTime():
                for i in range(num):
                    if not self.cron_run: break
                    time.sleep(1)
                    today = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))).strftime('\r%Y-%m-%dT%H:%M:%S (%%5d/%%-5d) ') % (i+1, num-i-1)
                    print(today, end='\b'*14)
                else:
                    if self.cron_fn:
                        self.cron_fn()
                    else:
                        print("do something and sleep", num, "second(s).")
            print("Exit CronWork.", ' '*10, '\b'*10)

    def CommandLoop(self):
        while self.cron_run:
            cmd = input(' ')
            if cmd.lower() in ["stop", "exit", "quit", "q"]:
                self.cron_run = False
                self.cron_thread.join()
                break
            elif cmd.lower() in ["look", "l", "ls"]:
                print("\ncron times:", self.cron_times)
            else:
                try:
                    num = int(cmd)
                    if num > 0:
                        self.cron_times.append(num)
                        print("\ncron times:", self.cron_times)
                except:
                    pass

if __name__ == '__main__':
    # enter your email and password
    v = v2ex(email, password)
    CronWork(v.daily).Run()
