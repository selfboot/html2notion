from urllib.parse import urlparse


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


if __name__ == '__main__':
    print(is_valid_url("https://www.google.com"))  # Returns: True
    print(is_valid_url("google"))  # Returns: False
