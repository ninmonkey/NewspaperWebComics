# NewspaperWebComics

if this app breaks, edit config.json with new CSS selectors


# example `config.js` entry

    "xkcd": {
        "url": "https://xkcd.com/",
        "class": null,
        "selectors": {
            "image": "#comic img",
            "comic_title": "#ctitle",
            "prev": "a[rel='prev']"
        }
    }

required:

    image: CSS selector to grab `<img>` element

optional:

    comic_title: CSS selector to grab comic title element. Fallback to `image.alt`
    class: name of class in CSS for special markup on a single comic
    prev: CSS selector for url to prev page

# bugfix

# todo

- auto-free space in /cache/ as needed
- why did image['title'] fail?
    - allow it to be optional like `alt`
        - need dict.get()
    - related to using html5lib ?
    - test on: http://www.qwantz.com/

- screenshot for github

- show 'new' images based on 
    - a local cookie or html5 storage
    
- optionally: specify order of comics displayed
- module js pattern
    - de-duplicate code in js init handlers
    - unused: handle_swap(), init()

- generate_js
    - use more data: title, alt, src, 
    
- cache.py
    remove all print statements for a STDOUT logger


- timed failure if thread is timing out eg. exception
- horizontal image center?
- move html output to /html/

- threading
    - need request_cached or anything that touches cache.json ?
    
- utilize `srcset` ?

- default selectors if config fails
    - images:
        "#comic img", "#cc-comic img", "img#comic", "img#cc-comic"
    - prev:
        "a[rel='prev']", "a.navi-prev", "a.prev"

    
# if dynamic site

- display 'new comic'
    - hide read images next time. (can't if static?)
    - auto-mark comics as read when scrolled to
        - read comics will auto-collapse or use lower opacity
