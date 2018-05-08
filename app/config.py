config = {
    "xkcd": {
        'url': 'https://xkcd.com/',
        'selectors': {
            'image': '#comic img',
            'comic_title': '#ctitle',
        }
    },
    "Penny Arcade": {
        'url': 'https://www.penny-arcade.com/comic',
        'selectors': {
            'image': '#comicFrame img',
            'comic_title': '#comic div div h2',
        }
    },
}
