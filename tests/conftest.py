import pytest


def pytest_addoption(parser):
    parser.addoption("--allow_api_call", action="store_true", default=False, help="Do the tests calling "
                                                                                  "the Twitter API")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--allow_api_call"):
        return
    skip_api_call = pytest.mark.skip(reason="need --allow_api_call option to run")
    for item in items:
        if "api_call" in item.keywords:
            item.add_marker(skip_api_call)

