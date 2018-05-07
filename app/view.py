from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def render(**kwargs):
    template = env.get_template('main.jinja2')
    return template.render(html='<h1>hi</h1>')
