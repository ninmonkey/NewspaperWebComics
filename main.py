import requests
from bs4 import BeautifulSoup

from cache import request_cached

# r = requests.get('http://explosm.net/comics/4922/')
# print(r.text)

# todo: try html5 parser

html_xkcd = request_cached('https://xkcd.com/1912/')
# print(html_xkcd)


html_pa = request_cached('https://www.penny-arcade.com/comic')
# write as cached curent date temp name

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