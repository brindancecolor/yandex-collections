import re
import json


class Link:

    def __init__(self, auth, link, collection_url):
        self.auth = auth
        self.collection_url = collection_url
        self.link = link
        self.get_collection_id(collection_url)
        # self.create()

    def get_collection_id(self, collection_url):
        self.auth.s.headers = self.auth.headers_default
        # r = self.auth.s.get(collection_url)
        r = self.auth.s.get(collection_url, verify=False)
        self.collection_id = re.search(r'boardId=(.*?)/', r.text).group(1)
        self.req_id = re.search(r'reqId\":\"(.*?)\"', r.text).group(1)

        url_json = re.search(r'cardSimilar\":({.*?})\,', r.text).group(1)
        url_json = re.search(r'_query\":(.*)', url_json).group(1)
        print(url_json)
        url_p = json.loads(url_json)
        url = f'https://yandex.ru/collections/api/cards?source_name=collections&ui=desktop&page={url_p["page"]}&page_size={url_p["page_size"]}&seed={url_p["seed"]}&similar_to_board={url_p["similar_to_board"]}'
        self.auth.s.headers.update({
            'Accept': '*/*',
            'x-req-id': self.req_id,
            'Upgrade-Insecure-Requests': None
        })
        # r = self.auth.s.get(url)
        r = self.auth.s.get(url, verify=False)
        self.csrf_token = r.headers['x-csrftoken']
        print(r.json())

    def create(self):
        url_options = 'https://collections.yandex.ru/collections/api/pages/parse/?source_type=link&source_name=collections&ui=desktop'
        headers = {
            'Accept': '*/*',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type,x-csrftoken,x-req-id',
            'Referer': self.collection_url,
            'Origin': 'https://yandex.ru',
            'Cache-Control': 'max-age=0',
        }
        self.auth.s.headers.update(headers)
        # r = self.auth.s.options(url_options)
        r = self.auth.s.options(url_options, verify=False)

        url_post1 = 'https://collections.yandex.ru/collections/api/pages/parse/?source_type=link&source_name=collections&ui=desktop'
        headers = {
            'Access-Control-Request-Method': None,
            'Access-Control-Request-Headers': None,
            'Content-Type': 'application/json; charset=utf-8',
            'x-csrftoken': self.csrf_token,
            'x-req-id': self.req_id,
        }
        self.auth.s.headers.update(headers)
        payload = {'url': self.link}
        # r = self.auth.s.post(url_post1, json=payload)
        # r = self.auth.s.post(url_post1, json=payload, verify=False)
        # print(r.json())

        url_post2 = 'https://yandex.ru/collections/api/v1.0/cards/?as_company=company%40smolmonument&source_name=collections&ui=desktop'
        payload = {
            'labels': [],
            'title': 'dfsfefwef',
            # 'title': r.json()['title'],
            'description': 'sdfwrrggergreg',
            # 'description': r.json()['description'],
            'content': [{'source_type': 'link', 'source': {
                'url': self.link,
                'preview': 'https://smolmonument.ru/uploads/product/58c7cf7c910b5_prv.jpg'
            }}],
            'board_id': self.collection_id
        }
        # r = self.auth.s.post(url_post2, json=payload)
        r = self.auth.s.post(url_post2, json=payload, verify=False)
        print(r.json())
