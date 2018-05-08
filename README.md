# NewspaperWebComics

if this app breaks, edit config.json with new CSS selectors

# todo

- why does image['title'] fail?
    - related to using html5lib ?
    
- make image url use cache images
- move html output to /html/
- make array of dicts passed to render
- should I strip `//` prefixes?
    - eg: //imgs.xkcd.com/comics/thermostat.png
- horizontal image center
- throttle requests to same domain
- autogen root path based on location
- redownload cached HTML if older than Xdays/Xhours