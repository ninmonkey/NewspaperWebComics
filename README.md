# NewspaperWebComics

if this app breaks, edit config.json with new CSS selectors


# example `config.js` entry

    "xkcd": {
        "url": "https://xkcd.com/",
        "class": null,
        "selectors": {
            "image": "#comic img",
            "comic_title": "#ctitle"
        }
    }

required:

    image: CSS selector to grab `<img>` element

optional:

    comic_title: CSS selector to grab comic title element. Fallback to `image.alt`
    class: name of class in CSS for special markup on a single comic

# first

Debug. Fix

# todo

- module js pattern
- de-duplicate code in js init handlers
- async request fetch of urls?

- why does image['title'] fail?
    - allow it to be optional like `alt`
        - need dict.get()
    - related to using html5lib ?
    - test on: http://www.qwantz.com/

- horizontal image center
- move html output to /html/

- auto-free space in /cache/ as needed

- utilize `srcset` ?

- default selectors if config fails
    "#comic img", "#cc-comic img", "img#comic", "img#cc-comic"

# if dynamic site

- display 'new comic'
    - hide read images next time. (can't if static?)
    - auto-mark comics as read when scrolled to
        - read comics will auto-collapse or use lower opacity
