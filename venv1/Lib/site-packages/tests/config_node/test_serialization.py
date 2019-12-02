import datetime
import pickle
import msgpack

from python_json_config.config_node import ConfigNode


def test_pickle(config_dict):
    config = ConfigNode(config_dict)
    pickle_conf = pickle.loads(pickle.dumps(config))
    assert pickle_conf.key1 == 1
    assert pickle_conf.key2.key3 == 3
    assert pickle_conf.key2.key4.key5 == 5


def test_to_dict(config_dict):
    config = ConfigNode(config_dict)
    assert config.to_dict() == config_dict
    assert config.key2.to_dict() == config_dict["key2"]
    assert config.key2.key4.to_dict() == config_dict["key2"]["key4"]
    assert ConfigNode(config.to_dict()) == config


def test_to_json(config_dict):
    config = ConfigNode(config_dict)
    json = config.to_json()
    assert json == """{"key1": 1, "key2": {"key3": 3, "key4": {"key5": 5}, "key6": 6}, "key7": 7}"""


def test_to_json_complex_types(config_dict):
    config = ConfigNode({
        "key1": datetime.timedelta(seconds=1, minutes=2),
        "key2": datetime.datetime(day=1, year=2000, month=4)
    })
    json = config.to_json()
    assert json == """{"key1": "0:02:01", "key2": "2000-04-01 00:00:00"}"""


def test_to_msgpack(config_dict):
    config = ConfigNode(config_dict)
    deserialized_dict = msgpack.loads(config.to_msgpack(), raw=False)
    assert deserialized_dict == config.to_dict()


def test_from_msgpack(config_dict):
    config = ConfigNode(config_dict)
    serialized = config.to_msgpack()
    deserialized_config = ConfigNode.from_msgpack(serialized)
    assert config == deserialized_config


def test_to_msgpack_complex_type():
    config = ConfigNode({
        "key1": datetime.timedelta(seconds=1, minutes=2),
        "key2": datetime.datetime(day=1, year=2000, month=4)
    })
    deserialized_dict = msgpack.loads(config.to_msgpack(), raw=False)
    assert deserialized_dict == {"key1": "0:02:01", "key2": "2000-04-01 00:00:00"}


def test_from_msgpack_complex_type():
    config = ConfigNode({
        "key1": datetime.timedelta(seconds=1, minutes=2),
        "key2": datetime.datetime(day=1, year=2000, month=4)
    })
    deserialized_config = ConfigNode.from_msgpack(config.to_msgpack())
    assert deserialized_config == ConfigNode({"key1": "0:02:01", "key2": "2000-04-01 00:00:00"})
