from python_json_config.validators import is_timedelta, is_valid_choice


def test_is_timedelta():
    valid_timedeltas = ["1:3:24:30:23", "0:0:1", "0:0:0:0:1", "01:02:02:03:04"]
    invalid_timedeltas = ["1:3:24:30:23:45", "01:a:02:03:04"]

    for timedelta in valid_timedeltas:
        assert is_timedelta(timedelta)

    assert is_timedelta(invalid_timedeltas[0]) == (False, "Timedelta contains more than 5 elements.")
    assert is_timedelta(invalid_timedeltas[1]) == (False, "Timedelta contains non-integer elements.")


def test_is_valid_choice():
    list_options = [1, 2, "3"]
    list_validator = is_valid_choice(list_options)
    assert list_validator(1)
    assert list_validator(3) == (False, f"Value is not contained in the options {list_options}")
    assert list_validator("3")
    assert list_validator(4) == (False, f"Value is not contained in the options {list_options}")

    dict_options = {1: "2", "3": 4}
    dict_validator = is_valid_choice(dict_options)
    assert dict_validator(1)
    assert dict_validator("2") == (False, f"Value is not contained in the options {dict_options}")
    assert dict_validator("3")
    assert dict_validator(4) == (False, f"Value is not contained in the options {dict_options}")
