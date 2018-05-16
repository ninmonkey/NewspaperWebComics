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

    0] Stand Still. Stay Silent:, dinoaur comics, Gunnerkrigg, Shark Splode

    1]  nth-of-type says it works but it doesn't seem to 
    .navbar a:nth-of-type(2)      
    
    repl says
        
        >>> soup.select(".navbar a:nth-of-type(2)")[0].get('href')
        'index.php?id=304'

       "http://dawnoftimecomics.com/": [
        {
            "comic_title": "Dawn of Time Strip #305 (July 4, 2011)",
            "image_src": "cache\\2018 05 14 - 16 41 29 519218.png"
        },
        {
            "comic_title": "Dawn of Time Strip #305 (July 4, 2011)",
            "image_src": "cache\\2018 05 14 - 16 41 29 519218.png"
        },
        {
            "comic_title": "Dawn of Time Strip #305 (July 4, 2011)",
            "image_src": "cache\\2018 05 14 - 16 41 29 519218.png"


# todo

- screenshot for github

- threading
    - might need further locks such as config read/write
    
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
    - images:
        "#comic img", "#cc-comic img", "img#comic", "img#cc-comic"
    - prev:
        "a[rel='prev']", "a.navi-prev", "a.prev"

# if dynamic site

- display 'new comic'
    - hide read images next time. (can't if static?)
    - auto-mark comics as read when scrolled to
        - read comics will auto-collapse or use lower opacity
