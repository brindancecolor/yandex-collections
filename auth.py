# coding:utf-8

import re
import requests

proxies = {
    'http': '127.0.0.1:8888',
    'https': '127.0.0.1:8888'
}


class Authentication:

    def __init__(self, login, password, headers):
        self.s = requests.Session()
        self.headers_default = headers
        self.s.headers.update(self.headers_default)
        self.s.proxies.update(proxies)
        self.login = login
        self.password = password
        self.req_passport()
        self.req_start()
        self.req_commit()
        self.req_accounts()

    def req_passport(self):
        url = 'https://passport.yandex.ru/auth'
        # r = self.s.get(url)
        r = self.s.get(url, verify=False)
        self.csrf_token = re.search(r'data-csrf="(.*?)"', r.text).group(1)
        self.process_uuid = re.search(r'process_uuid=(.*?)"', r.text).group(1)

    def req_start(self):
        url = 'https://passport.yandex.ru/registration-validations/auth/multi_step/start'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://passport.yandex.ru/auth',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://passport.yandex.ru'
        }
        self.s.headers.update(headers)
        payload = {'csrf_token': self.csrf_token, 'login': self.login, 'process_uuid': self.process_uuid}
        # r = self.s.post(url, data=payload)
        r = self.s.post(url, data=payload, verify=False)
        # print(r.json())
        self.track_id = r.json()['track_id']

    def req_commit(self):
        url = 'https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password'
        headers = {'Referer': 'https://passport.yandex.ru/auth/welcome'}
        self.s.headers.update(headers)
        payload = {'csrf_token': self.csrf_token, 'track_id': self.track_id, 'password': self.password}
        # r = self.s.post(url, data=payload)
        r = self.s.post(url, data=payload, verify=False)
        # print(r.json())
        self.ok = r.json()['status']

    def req_accounts(self):
        url = 'https://passport.yandex.ru/registration-validations/auth/accounts'
        payload = {'csrf_token': self.csrf_token}
        # r = self.s.post(url, data=payload)
        r = self.s.post(url, data=payload, verify=False)
        # print(r.json())
        self.uid = r.json()['accounts']['authorizedAccounts'][0]['uid']
