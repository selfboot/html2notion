from urllib.parse import urlparse


def is_valid_url(url):
    if not isinstance(url, str):
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and is_valid_port(result.port)
    except ValueError:
        return False


def is_valid_port(port):
    if port is None:
        return True
    return 0 <= port <= 65535


if __name__ == '__main__':
    print(is_valid_url("https://www.google.com"))  # Returns: True
    print(is_valid_url("google"))  # Returns: False
