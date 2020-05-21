import configparser
import ssl

from auth import Authentication
from links import Link
# from colls import Collection

ssl._create_default_https_context = ssl._create_unverified_context


def main():

    # получим логин, пароль из файла auth.ini
    auth = configparser.ConfigParser()
    auth.optionxform = str
    auth.read('auth.ini')

    settings = configparser.ConfigParser()
    settings.optionxform = str
    settings.read('settings.ini')

    # создадим объект аторизации
    a = Authentication(
        auth['Authorization']['Login'],
        auth['Authorization']['Password'],
        dict(settings['Browser Headers'])
    )
    print(a.uid)

    # создадим объект коллекции
    # c = Collection(a)
    # print(c.req_id, c.csrf_token, sep='\n')
    # new_coll = c.create('new-coll1', 'description new-coll1')

    # создадим карточку-ссылку
    link = 'https://zip-sm.ru/product/mufta-motora-kuhonnogo-kombajna-kenwood'
    collection_url = 'https://yandex.ru/collections/user/company%40zip/mekhanika-dlia-blenderov-zapchasti-dlia-miasorubok-i-blenderov/'
    l = Link(a, link, collection_url)
    print(l.link, l.collection_url, l.collection_id, sep='\n')


if __name__ == "__main__":
    main()
    # pass
