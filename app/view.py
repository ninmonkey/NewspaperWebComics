from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def render(comic_kwargs):
    template = env.get_template('main.jinja2')
    print(comic_kwargs)
    # print(comic_kwargs['header'])
    return template.render(comic=comic_kwargs)
