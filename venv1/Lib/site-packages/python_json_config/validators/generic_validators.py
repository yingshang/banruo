from typing import Union, Tuple


def is_timedelta(value: str) -> Union[bool, Tuple[bool, str]]:
    """
    Tests if the given value is a valid timedelta specification.
    The timedelta needs to be specified as a colon separated string, e.g.: "0:0:23:00:00"
        The format is as follows "WW:DD:HH:MM:SS"
        W = number of months
        D = number of days
        H = number of hours
        M = number of minutes
        S = number of seconds
    :param value: The timedelta as string.
    :return: True if the value is a valid timedelta specification otherwise False.
    """
    split_values = value.split(":")
    if len(split_values) > 5:
        return False, "Timedelta contains more than 5 elements."

    try:
        [int(element) for element in split_values]
    except ValueError:
        return False, "Timedelta contains non-integer elements."

    return True


def is_valid_choice(options):
    """
    Returns a function that tests if the config value is an element of the passed options.
    :param options: The options that are considered as valid choices.
    :return: A functions that takes a value and tests if it is within the specified choices. This function returns True
             if the value in the config is in the passed options.
    """
    def validator(value) -> Tuple[bool, str]:
        return value in options, f"Value is not contained in the options {options}"

    return validator
