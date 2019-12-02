from python_json_config.config_node import ConfigNode


def test_contains(config_dict):
    config = ConfigNode(config_dict)
    assert "key1" in config
    assert "key1.key2" not in config
    assert "key2.key3" in config
    assert "key2.key4.key5" in config
    assert "key2.key4.key6" not in config


def test_keys(config_dict):
    config = ConfigNode(config_dict)
    keys = list(config.keys())
    expected_keys = ["key1", "key2.key3", "key2.key4.key5", "key2.key6", "key7"]
    assert keys == expected_keys


def test_values(config_dict):
    config = ConfigNode(config_dict)
    values = list(config.values())
    assert values == [1, 3, 5, 6, 7]


def test_items(config_dict):
    config = ConfigNode(config_dict)
    items = list(config.items())
    expected_items = [("key1", 1), ("key2.key3", 3), ("key2.key4.key5", 5), ("key2.key6", 6), ("key7", 7)]
    assert items == expected_items


def test_iter(config_dict):
    config = ConfigNode(config_dict)
    expected_keys = ["key1", "key2.key3", "key2.key4.key5", "key2.key6", "key7"]
    assert list(config) == expected_keys


def test_iteration(config_dict):
    config = ConfigNode(config_dict)
    for iter_key, key, value, item in zip(config, config.keys(), config.values(), config.items()):
        item_key, item_value = item
        assert iter_key == key
        assert item_key == key
        assert item_value == value
        assert config.get(key) == value
