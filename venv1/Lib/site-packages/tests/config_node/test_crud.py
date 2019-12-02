import os
import warnings
import pytest

from python_json_config.config_node import ConfigNode


def test_creation(config_dict):
    node = ConfigNode(config_dict)
    assert node.key1 == 1
    assert node.__dict__["_ConfigNode__path"] == []
    assert isinstance(node.key2, ConfigNode)

    nested_node = node.key2
    assert nested_node.key3 == 3
    assert nested_node.__dict__["_ConfigNode__path"] == ["key2"]
    assert isinstance(nested_node.key4, ConfigNode)

    nested_node = nested_node.key4
    assert nested_node.key5 == 5
    assert nested_node.__dict__["_ConfigNode__path"] == ["key2", "key4"]


def test_get(config_dict):
    node = ConfigNode(config_dict)
    assert node.key1 == 1
    with pytest.raises(AttributeError):
        node.nokey

    assert node.get("key1") == 1
    with pytest.raises(AttributeError):
        node.get("nokey")

    assert node.get("key2.key3") == 3


def test_add():
    node = ConfigNode({"key1": 1})
    assert node.key1 == 1

    with pytest.raises(AttributeError):
        node.key2
    node.add("key2", 2)
    assert node.key2 == 2

    with pytest.raises(AttributeError):
        node.key3.key4
    node.add("key3.key4", "test")
    assert node.key3.key4 == "test"


def test_add_overwrite():
    node = ConfigNode({"key1": 1})
    assert node.key1 == 1

    with warnings.catch_warnings(record=True) as warning_log:
        assert len(warning_log) == 0

        node.add("key1", 2, overwrite=False)
        assert len(warning_log) == 1
        assert node.key1 == 2

        node.add("key1", 3)
        assert len(warning_log) == 1
        assert node.key1 == 3


def test_update(config_dict):
    node = ConfigNode(config_dict)

    assert node.key1 == 1
    node.update("key1", 2)
    assert node.key1 == 2

    node.update("key1", {"newkey": 1})
    assert isinstance(node.key1, ConfigNode)
    assert node.key1.newkey == 1

    assert isinstance(node.key2.key4, ConfigNode)
    node.update("key2.key4", 1337)
    assert node.key2.key4 == 1337


def test_upsert():
    node = ConfigNode({"key1": 1})

    with pytest.raises(AttributeError):
        node.key2

    with pytest.raises(RuntimeError):
        node.update("key2", "asd", upsert=False)

    node.update("key2", "asd", upsert=True)
    assert node.key2 == "asd"


def test_nested_update():
    node = ConfigNode({"key1": 1})

    with pytest.raises(AttributeError):
        node.key2

    with pytest.raises(RuntimeError):
        node.update("key2.key3", "asd", upsert=False)


def test_nested_upsert():
    node = ConfigNode({"key1": 1})

    with pytest.raises(AttributeError):
        node.key2

    node.update("key2.key3", "asd", upsert=True)
    assert node.key2.key3 == "asd"


def test_strict_access(config_dict):
    config = ConfigNode(config_dict,
                        strict_access=True,
                        optional_fields=["nokey", ["key2", "nokey"], "key2.nokey2"])
    assert config.nokey is None
    assert config.key2.nokey is None
    assert config.key2.nokey2 is None
    with pytest.raises(AttributeError):
        config.key2.nokey3

    config = ConfigNode(config_dict,
                        strict_access=False,
                        required_fields=["nokey", ["key2", "nokey"], "key2.nokey2"])
    assert config.key2.nokey3 is None
    with pytest.raises(AttributeError):
        assert config.nokey is None
    with pytest.raises(AttributeError):
        assert config.key2.nokey is None
    with pytest.raises(AttributeError):
        assert config.key2.nokey2 is None


def test_merge_env_variable():
    prefix = "PYTHONJSONCONFIG"
    variables = {f"{prefix}_TESTVALUE1": "bla", f"{prefix}_TESTVALUE2": "1"}
    for key, value in variables.items():
        os.environ[key] = value

    invalid_prefix = "PYTHONJSONCONFIGTEST"
    os.environ[invalid_prefix] = "invalid"

    config = ConfigNode({"testvalue1": "blub", "testvalue3": 5})
    config.merge_with_env_variables(prefix)

    assert config.testvalue1 == "bla"
    assert config.testvalue2 == "1"
    assert config.testvalue3 == 5
    assert "test" not in config

    for key, value in variables.items():
        del os.environ[key]
