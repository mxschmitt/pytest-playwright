import pytest
import playwright
from _pytest.config.argparsing import Parser

import asyncio


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def launch_browser(pytestconfig):
    browser_name = pytestconfig.getoption("browser")

    async def launch(**kwargs):
        return await playwright.browser_types[browser_name].launch(**kwargs)

    return launch


@pytest.fixture(scope="session")
async def browser(launch_browser):
    browser = await launch_browser()
    yield browser
    await browser.close()


@pytest.fixture
async def context(browser):
    context = await browser.newContext()
    yield context
    await context.close()


@pytest.fixture
async def page(context):
    page = await context.newPage()
    yield page
    await page.close()


def pytest_addoption(parser: Parser):
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser engine which should be used",
    )
