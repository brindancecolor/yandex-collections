import re


class Collection:

    def __init__(self, auth):
        self.auth = auth
        self.req_collectiond()
        self.api_user()

    def req_collectiond(self):
        url = 'https://yandex.ru/collections/'
        self.auth.s.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': None,
            'Content-Type': None,
            'X-Requested-With': None,
            'Origin': None
        })
        # r = self.auth.s.get(url)
        r = self.auth.s.get(url, verify=False)
        self.req_id = re.search(r'reqId":"(.*?)"', r.text).group(1)

    def api_user(self):
        url = 'https://yandex.ru/collections/api/user/?source_name=collections&ui=desktop'
        self.auth.s.headers.update({
            'Accept': '*/*',
            'Referer': 'https://yandex.ru/collections/',
            'Content-Type': 'application/json; charset=utf-8',
            'x-req-id': self.req_id,
            'Origin': 'https://yandex.ru',
            'Cache-Control': 'max-age=0'
        })
        payload = {'preferences': {'general': {
            'ei_guide_cards_step': -1,
            'show_coauthor_tooltip': -1,
            'ei_coauthors_recent': 0,
            'guide_edit_profile': -1
        }}}
        # r = self.auth.s.patch(url, json=payload)
        r = self.auth.s.patch(url, json=payload, verify=False)
        self.csrf_token = r.json()['csrf-token']

    def get_collection_id(self, collection_url):

    def create(self, title, description):
        url = 'https://yandex.ru/collections/api/boards/?source_name=collections&ui=desktop'
        self.auth.s.headers.update({
            'x-csrftoken': self.csrf_token,
            'x-req-id': self.req_id,
            'Cache-Control': None,
            'Upgrade-Insecure-Requests': None
        })
        payload = {
            'title': title, 'description': description,
            'is_private': False, 'is_wishlist': False
        }
        # r = self.auth.s.post(url, json=payload)
        r = self.auth.s.post(url, json=payload, verify=False)
        print(r.json())
