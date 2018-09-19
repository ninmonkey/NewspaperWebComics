import threading
from urllib.parse import urljoin


class ComicListThreaded:
    def __init__(self):
        self.comics = []
        self.lock = threading.Lock()

    def extend(self, comics):
        with self.lock:
            self.comics.extend(comics)


def grab_attr(soup, selector, attr):
    # return one or None
    element = soup.select(selector)
    if element:
        return element[0].get(attr)

    return None


def grab_text(soup, selector):
    # return one or None
    if not selector:
        return ''

    element = soup.select(selector)
    if element:
        return element[0].text

    return ''


def get_full_url(url_html, url_image):
    # convert relative urls to fully resolvable url
    # (almost) not necessary, could use raw urljoins()
    url_html = url_html.strip()
    url_image = url_image.strip()
    if not url_html or not url_image:
        raise ValueError("Requires both html and img urls!")

    if url_html == url_image:
        return url_html

    return urljoin(url_html, url_image)


def humanize_bytes(num_bytes, suffix='B'):
    # convert byte count to human readable units
    num = num_bytes
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "{num:.2f}{unit}{suffix}".format(num=num, unit=unit, suffix=suffix)
        num /= 1024.0
    return "{num:.2f}{unit}{suffix}".format(num=num, unit='Yi', suffix=suffix)
