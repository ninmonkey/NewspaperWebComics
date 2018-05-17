from jinja2 import Environment, PackageLoader, select_autoescape
import json

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def generate_js(comics):
    js_offsets = {}
    js_comics = {}
    for group in comics:
        group_key = group[0]['comic_url']
        js_offsets[group_key] = 0
        js_comics[group_key] = []

        for comic in group:
            d = {
                "comic_title": comic['comic_title'],
                "image_src": comic['image_src'],
            }
            js_comics[group_key].append(d)

    return {
        "js_offsets": json.dumps(js_offsets, indent=4, sort_keys=True),
        "js_comics": json.dumps(js_comics, indent=4, sort_keys=True)
    }


def render(comics):
    template = env.get_template('main.jinja2')
    js_vars = generate_js(comics)
    return template.render(comics=comics, js_vars=js_vars)
