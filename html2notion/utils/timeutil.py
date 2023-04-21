from datetime import datetime


def DateStrToISO8601(date_string: str) -> str:
    """Converts a date string to ISO 8601 format.

    Args:
        date_string (str): Date string to convert.

    Returns:
        str: ISO 8601 formatted date string.
    """

    date_format = "%Y-%m-%d %H:%M:%S %z"
    date_obj = datetime.strptime(date_string, date_format)
    local_date_obj = date_obj.astimezone()
    output_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    output_string = local_date_obj.strftime(output_format)
    output_string = output_string[:-3] + "Z"
    return output_string