from asyncio.events import AbstractEventLoop
from typing import Any, Callable, Awaitable, AsyncGenerator, Dict, Generator, List
import asyncio

import pytest

import playwright
from playwright.page import Page
from playwright.browser import BrowserContext
from playwright.browser import Browser


def pytest_generate_tests(metafunc: Any) -> None:
    if "browser_name" in metafunc.fixturenames:
        browsers = metafunc.config.option.browser or ["chromium", "firefox", "webkit"]
        metafunc.parametrize("browser_name", browsers, scope="session")


@pytest.fixture(scope="session")
def browser_name(pytestconfig: Any) -> str:
    return pytestconfig.getoption("browser")


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def launch_arguments() -> Dict:
    return {}


@pytest.fixture(scope="session")
async def launch_browser(
    pytestconfig: Any, launch_arguments: Dict, browser_name: str
) -> Callable[..., Awaitable[Browser]]:
    async def launch(**kwargs: Dict[Any, Any]) -> Browser:
        headful_option = pytestconfig.getoption("--headful")
        launch_options = {**launch_arguments, **kwargs}
        if headful_option:
            launch_options["headless"] = False
        return await playwright.browser_types[browser_name].launch(**launch_options)

    return launch


@pytest.fixture(scope="session")
async def browser(
    launch_browser: Callable[[], Awaitable[Browser]]
) -> AsyncGenerator[Browser, None]:
    browser = await launch_browser()
    yield browser
    await browser.close()


@pytest.fixture
async def context(browser: Browser) -> AsyncGenerator[BrowserContext, None]:
    context = await browser.newContext()
    yield context
    await context.close()


async def _handle_page_goto(
    page: Page, args: List[Any], kwargs: Dict[str, Any], base_url: str
) -> None:
    url = args.pop()
    if not (url.startswith("http://") or url.startswith("https://")):
        url = base_url + url
    return await page._goto(url, *args, **kwargs)


@pytest.fixture
async def page(context: BrowserContext, base_url: str) -> AsyncGenerator[Page, None]:
    page = await context.newPage()
    page._goto = page.goto
    page.goto = lambda *args, **kwargs: _handle_page_goto(
        page, list(args), kwargs, base_url
    )
    yield page
    await page.close()


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--browser",
        action="append",
        default=[],
        help="Browser engine which should be used",
    )
    parser.addoption(
        "--headful",
        action="store_true",
        default=False,
        help="Run tests in headful mode.",
    )
