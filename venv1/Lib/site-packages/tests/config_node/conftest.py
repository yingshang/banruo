import pytest


@pytest.fixture(scope="session")
def config_dict() -> dict:
    return {
        "key1": 1,
        "key2": {
            "key3": 3,
            "key4": {"key5": 5},
            "key6": 6
        },
        "key7": 7
    }
