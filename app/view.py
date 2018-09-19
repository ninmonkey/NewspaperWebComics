from jinja2 import Environment, PackageLoader, select_autoescape
import json

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def generate_js(grouped_comics):
    js_offsets = {}
    js_comics = grouped_comics

    for key in grouped_comics.keys():
        js_offsets[key] = 0

    return {
        'js_offsets': json.dumps(js_offsets, indent=4, sort_keys=True),
        'js_comics': json.dumps(js_comics, indent=4, sort_keys=True)
    }


def group_comics(comics):
    js_comics = {}
    # for comic in comics:
    #     print(comic)

    groups = set()
    for comic in comics:
        comic_url = comic['comic_url']
        groups.add(comic_url)
        js_comics[comic_url] = []

    print("sets: ", groups)

    for group in groups:
        for comic in comics:
            comic_url = comic['comic_url']
            if comic_url == group:
                js_comics[comic_url].append(comic)

    return js_comics


def render(comics):
    comics_grouped = group_comics(comics)
    js_vars = generate_js(comics_grouped)
    template = env.get_template('main.jinja2')

    return template.render(comics=comics_grouped, js_vars=js_vars)


