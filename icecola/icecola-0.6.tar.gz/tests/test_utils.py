from icecola.crawler_utils.utils import random_user_agent


def test_random_useragent():
    assert random_user_agent()
