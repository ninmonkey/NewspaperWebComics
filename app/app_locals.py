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