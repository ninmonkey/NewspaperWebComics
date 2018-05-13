from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def render(comics):
    template = env.get_template('main.jinja2')
    for group in comics:
        print("1")
        print(group)
    return template.render(comics=comics)
