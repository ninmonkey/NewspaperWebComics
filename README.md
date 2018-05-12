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

# todo

async request fetch of urls?

first:
- display 'new comic'
    - read comics will auto-collapse or use lower opacity

- why does image['title'] fail?
    - related to using html5lib ?
    - test on: http://www.qwantz.com/
    - allow it to be optional like `alt`

- horizontal image center
- move html output to /html/

- throttle requests to same domain
- autogen root path based on location

- use HTTPS in `fetch_comic()`, fallback to HTTP
- utilize `srcset` ?

- auto-free space in /cache/ as needed

- default selectors if config fails
    "#comic img", "#cc-comic img", "img#comic", "img#cc-comic"

- 
# if dynamic site

- auto-mark comics as read when scrolled to

# bugfix:

    - DEBUG:root:relative url, New source = https://imgs.xkcd.com//comics/safetysat.png
