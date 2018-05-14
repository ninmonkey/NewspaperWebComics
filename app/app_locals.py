from urllib.parse import urlparse, urlunparse


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
    if not url_html or not url_image:
        raise ValueError("Requires both html and img urls!")

    if url_html == url_image:
        return url_html

    parsed_html = urlparse(url_html)
    parsed_image = urlparse(url_image)

    image_src_full = '{scheme}://{netloc}/{path}'.format(
        scheme=parsed_image.scheme or parsed_html.scheme or 'http',
        netloc=(parsed_image.netloc or parsed_html.netloc).rstrip('/'),
        path=parsed_image.path.strip().lstrip('/'),
        # 'params': parsed_image.params,
        # 'query': parsed_image.query,
        # 'fragment': parsed_image.fragment,
    )
    return image_src_full