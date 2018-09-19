from jinja2 import Environment, PackageLoader, select_autoescape
import json

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def generate_js(grouped_comics):
    js_offsets = {}
    js_comics = {}
    # for comic in comics:
    #     print(comic)
    #
    # groups = set()
    # for comic in comics:
    #     comic_url = comic['comic_url']
    #     groups.add(comic_url)
    #     js_comics[comic_url] = []
    #
    # print("sets: ", groups)
    #
    for group in grouped_comics:
        print("group: ", group)
        for comic in grouped_comics:
            comic_url = comic['comic_url']
            if comic_url == group:
                d = {
                    'comic_title': comic['comic_title'],
                    'image_src': comic['image_src'],
                    'comic_url': comic['comic_url'],
                    'has_prev': comic['has_prev'],
                }

                js_comics[comic_url].append(d)
                print(d)

    print("Js generate_js()")
    print(js_comics)

    return {
        'js_offsets': json.dumps(js_offsets, indent=4, sort_keys=True),
        'js_comics': json.dumps(js_comics, indent=4, sort_keys=True)
    }


def group_comics(comics):
    js_comics = {}
    for comic in comics:
        print(comic)

    groups = set()
    for comic in comics:
        comic_url = comic['comic_url']
        groups.add(comic_url)
        js_comics[comic_url] = []

    print("sets: ", groups)

    for group in groups:
        print("group: ", group)
        for comic in comics:
            comic_url = comic['comic_url']
            if comic_url == group:
                d = {
                    'comic_title': comic['comic_title'],
                    'image_src': comic['image_src'],
                    'comic_url': comic['comic_url'],
                    'has_prev': comic['has_prev'],
                }

                js_comics[comic_url].append(d)
                print(d)

    print("Js_grouped: ")
    print(js_comics)
    return js_comics


def render(comics):
    # js_vars = generate_js(comics)
    comics_grouped = group_comics(comics)
    print("yeah")
    print(comics_grouped)

    template = env.get_template('main.jinja2')
    js_vars = {
        "js_offsets": {},
        "js_comics": {},
    }


    return template.render(comics=comics_grouped, js_vars=js_vars)
    # return template.render(comics=comics_grouped, js_vars=js_vars)

