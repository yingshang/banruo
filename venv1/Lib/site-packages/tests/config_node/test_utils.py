from python_json_config.config_node import ConfigNode


def test_string():
    node = ConfigNode({1: 2, 3: 4})
    node_str = "ConfigNode(path=[], values={1: 2, 3: 4}, strict_access=True, required_fields=[], optional_fields" \
               "=[])"
    assert str(node) == node_str


def test_equality():
    node1 = ConfigNode({"a": 2, "b": 4})
    node2 = ConfigNode({"a": 2, "b": 4})
    node3 = ConfigNode({"a": 2, "c": 4})
    node4 = ConfigNode({"a": 2, "c": 5})
    assert node1 == node2
    assert node1 != node3
    assert node1 != node4
    assert node3 != node4
