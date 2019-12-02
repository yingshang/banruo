from python_json_config.validators import is_ipv4_address, is_unreserved_port


def test_is_ipv4_address():
    valid_ips = ["127.0.0.1", "8.8.8.8", "127.1", "8.526344"]
    invalid_ips = ["327.0.0.1", "8.8.8.8.8", "127.-1", "256.526344"]

    for address in valid_ips:
        assert is_ipv4_address(address)

    for address in invalid_ips:
        assert is_ipv4_address(address) == (False, "IP address is not a valid IPv4 address.")


def test_is_unreserved_port():
    assert is_unreserved_port(1) == (False, "Port is reserved.")
    assert is_unreserved_port(-1) == (False, "Port is reserved.")
    assert is_unreserved_port(22) == (False, "Port is reserved.")
    assert is_unreserved_port(1023) == (False, "Port is reserved.")
    assert is_unreserved_port(1024)
    assert is_unreserved_port(14302)
