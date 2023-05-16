from html2notion.utils import DateStrToISO8601, is_valid_url


def test_date_to_ios8601():
    valid_date_pair = {"2018-09-20 10:30:36 +0000": "2018-09-20T18:30:36+08:00",
                       "2023-05-12 03:49:56 +0000": "2023-05-12T11:49:56+08:00"}

    for date_string, expected in valid_date_pair.items():
        assert DateStrToISO8601(date_string) == expected

    invalid_date_pair = ["2018-09-20 10:30", "2018-09-20 10:30:36", "2018-09-20 10:30:36+0800"]
    for date_string in invalid_date_pair:
        assert DateStrToISO8601(date_string) == ""


def test_is_valid_url():
    valid_urls = [
        "http://www.example.com",
        "https://www.example.com",
        "ftp://www.example.com",
        "http://localhost",
        "http://127.0.0.1",
        "http://example.com/path?query#fragment",
    ]

    invalid_urls = [
        "example.com",
        "www.example.com",
        "http://",
        "http:///example.com",
        "http://example.com:80:80",  # Two port numbers
        None,
        123,  # Non-string input
        "",
    ]

    for url in valid_urls:
        assert is_valid_url(url) == True, f"Expected {url} to be valid"

    for url in invalid_urls:
        assert is_valid_url(url) == False, f"Expected {url} to be invalid"


if __name__ == '__main__':
    test_date_to_ios8601()
