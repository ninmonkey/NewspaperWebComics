from jinja2 import Environment, PackageLoader, select_autoescape
import json

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def generate_js(comics):
    js_offsets = {}
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

    print("Js")
    print(js_comics)




    # for group in comics:
    #     if not group:
    #         continue
    #
    #     group_key = group['comic_url']
    #     print(group_key)
    #     print(group)
    #     js_offsets[group_key] = 0
    #     js_comics[group_key] = []
    #
    #     for comic in group:
    #         d = {
    #             'comic_title': comic['comic_title'],
    #             'image_src': comic['image_src'],
    #             'comic_url': comic['comic_url'],
    #             'has_prev': comic['has_prev'],
    #         }
    #         # js_comics[group_key].append(d)
    #         # js_comics.append(d)

    return {
        'js_offsets': json.dumps(js_offsets, indent=4, sort_keys=True),
        'js_comics': json.dumps(js_comics, indent=4, sort_keys=True)
    }


def render(comics):
    template = env.get_template('main.jinja2')
    js_vars = generate_js(comics)
    return template.render(comics=comics, js_vars=js_vars)
