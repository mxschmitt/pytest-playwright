import pytest
import playwright
from _pytest.config.argparsing import Parser

@pytest.fixture(scope="session")
async def browser(pytestconfig):
    browser_name = pytestconfig.getoption("browser")
    browser = await playwright.browser_types[browser_name].launch()
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

def pytest_addoption(parser:Parser):
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help='Browser engine which should be used',
    )
