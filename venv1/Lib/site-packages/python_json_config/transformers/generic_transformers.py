from datetime import timedelta


def to_timedelta(value: str):
    """
    Converts the given value into a timedelta object.
    The timedelta needs to be specified as a colon separated string, e.g.: "0:0:23:00:00"
        The format is as follows "WW:DD:HH:MM:SS"
        W = number of months
        D = number of days
        H = number of hours
        M = number of minutes
        S = number of seconds

    :param value: The timedelta as string.
    :return: A timedelta value representing the timespan that is specified.
    """
    split_values = value.split(":")

    try:
        int_values = [int(element) for element in split_values]
    except ValueError:
        return None

    if len(int_values) <= 5:
        padded_values = [0] * (5 - len(int_values)) + int_values
        return timedelta(
            weeks=padded_values[0],
            days=padded_values[1],
            hours=padded_values[2],
            minutes=padded_values[3],
            seconds=padded_values[4],
        )
