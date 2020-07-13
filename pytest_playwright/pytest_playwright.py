from asyncio.events import AbstractEventLoop
from typing import Any, Callable, Awaitable, AsyncGenerator, Dict, Generator
import asyncio

import pytest

import playwright
from playwright.page import Page
from playwright.browser import BrowserContext
from playwright.browser import Browser


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
    pytestconfig: Any, launch_arguments: Dict
) -> Callable[..., Awaitable[Browser]]:
    browser_name = pytestconfig.getoption("browser")

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


@pytest.fixture
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    page = await context.newPage()
    yield page
    await page.close()


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser engine which should be used",
    )
    parser.addoption(
        "--headful",
        action="store_true",
        default=False,
        help="Run tests in headful mode.",
    )
