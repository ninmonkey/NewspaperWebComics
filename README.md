# NewspaperWebComics

if this app breaks, edit config.json with new CSS selectors

# todo

- redownload cached HTML if older than Xdays/Xhours
- convert config.py to config.json

- request_cached()
    - use mime type to detect html/image
    - reading cache needs modebinary when not HTML
- why does image['title'] fail?
    - related to using html5lib ?

- move html output to /html/
- horizontal image center
- throttle requests to same domain
- autogen root path based on location

- should I keep stripping `//` prefixes?
    - eg: //imgs.xkcd.com/comics/thermostat.png