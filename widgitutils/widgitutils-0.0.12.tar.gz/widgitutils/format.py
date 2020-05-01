from urllib.parse import urlparse


def trailingslashit(string=""):
    """
    Removes trailing forward slashes and backslashes if they exist.
    """

    return "{}/".format(string.strip("/\\"))


def valid_url(url="", schemas=None, context=None):
    """
    Validates a given URL against given schemas.
    """

    is_valid_url = False
    valid_image = ["gif", "jpg", "jpeg", "png"]

    if not schemas or type(schemas) is not dict:
        schemas = ["http", "https"]

    try:
        result = urlparse(url)

        if result.scheme in schemas:
            if not context:
                is_valid_url = True

            if context:
                last = url.rsplit(".").pop()

                is_valid_url = last in valid_image

        return is_valid_url
    except ValueError:
        return is_valid_url
