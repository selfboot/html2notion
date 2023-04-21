from datetime import datetime


def DateStrToISO8601(date_string: str) -> str:
    """Converts a date string to ISO 8601 format.

    Args:
        date_string (str): Date string to convert.

    Returns:
        str: ISO 8601 formatted date string.
    """

    date_format = "%Y-%m-%d %H:%M:%S %z"
    date_obj = datetime.strptime(date_string, date_format).astimezone()
    output_string = date_obj.isoformat()
    return output_string