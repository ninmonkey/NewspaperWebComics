import requests
from bs4 import BeautifulSoup

import cache

# r = requests.get('http://explosm.net/comics/4922/')
# print(r.text)

# todo: try html5 parser

cache.path_root ='C:\\Users\\cppmo_000\\Documents\\2018\\NewspaperWebComics\\cache'
cache.init_cache()

html_xkcd = cache.request_cached('https://xkcd.com/1912/')
html_pa = cache.request_cached('https://www.penny-arcade.com/comic')
# print(html_pa)

# xkcd
# soup = BeautifulSoup(html['xkcd'], 'html.parser')
# elem_comic = soup.find(id='comic')
# comic = {
#     'url': 'https://xkcd.com/1912/',
#     'src': elem_comic.img['src'],
#     'alt': elem_comic.img['alt'],
#     'title': elem_comic.img['title'],
# }
# print(comic)

# CnH

# elem_comic = soup.find(id='comic-wrap')
# comic = {
#     'url': 'http://explosm.net/comics/4922/',
#     'src': elem_comic.img['src'],
# }
# print(comic)


print('done')