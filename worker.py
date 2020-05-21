import configparser
import ssl

from auth import Authentication
# from colls import Collection
# from links import Link

ssl._create_default_https_context = ssl._create_unverified_context


def main():

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read('settings.ini')

    # создадим объект аторизации
    a = Authentication(
        config['Authorization']['Login'],
        config['Authorization']['Password'],
        dict(config['Browser Headers'])
    )
    print(a.uid)

    # создадим объект коллекции
    # c = Collection(a)
    # print(c.req_id, c.csrf_token, sep='\n')
    # new_coll = c.create('new-coll1', 'description new-coll1')

    # l = Link(a, link, collection_url)
    # print(l)


if __name__ == "__main__":
    main()
    # pass