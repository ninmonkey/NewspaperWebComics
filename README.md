# NewspaperWebComics

if this app breaks, edit config.json with new CSS selectors

# todo

change request_cached() depending on content type 'text/html' else binary

- randomize order
- horizontal image center
- redownload cached HTML if older than Xdays/Xhours

- request_cached()
    - use mime type to detect html/image
    - reading cache needs modebinary when not HTML
- why does image['title'] fail?
    - related to using html5lib ?

- move html output to /html/
- throttle requests to same domain
- autogen root path based on location

- should I keep stripping `//` prefixes?
    - eg: //imgs.xkcd.com/comics/thermostat.png

- use HTTPS in `fetch_comic()`, fallback to HTTP
