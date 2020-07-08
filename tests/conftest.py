pytest_plugins = ["pytester"]

import pytest
import playwright

@pytest.fixture(scope="session")
def event_loop(request):
    loop = playwright.playwright.loop
    yield loop
    loop.close()
