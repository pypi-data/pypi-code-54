from helloworld import say_hello


def test_helloworld_no_param():
    assert say_hello() == "hello, world!"


def test_helloworld_param():
    assert say_hello("everyone") == "hello, everyone!"