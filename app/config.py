config = {
    "xkcd": {
        'url': 'https://xkcd.com/',
        'class': None,
        'selectors': {
            'image': '#comic img',
            'comic_title': '#ctitle',
        }
    },
    "Penny Arcade": {
        'url': 'https://www.penny-arcade.com/comic',
        'class': 'comic_PA',
        'selectors': {
            'image': '#comicFrame img',
            'comic_title': '#comic div div h2',
        }
    },
}
