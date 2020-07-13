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
        browsers = metafunc.config.option.browser or ["chromium"]
        metafunc.parametrize("browser_name", browsers, scope="session")


def pytest_configure(config: Any) -> None:
    config.addinivalue_line(
        "markers", "skip_browser(name): mark test to be skipped a specific browser"
    )
    config.addinivalue_line(
        "markers", "only_browser(name): mark test to run only on a specific browser"
    )


def _get_skiplist(request: Any, values: List[str], value_name: str) -> List[str]:
    skipped_values: List[str] = []
    # Allowlist
    only_marker = request.node.get_closest_marker(f"only_{value_name}")
    if only_marker:
        skipped_values = values
        skipped_values.remove(only_marker.args[0])

    # Denylist
    skip_marker = request.node.get_closest_marker(f"skip_{value_name}")
    if skip_marker:
        skipped_values.append(skip_marker.args[0])

    return skipped_values


@pytest.fixture(autouse=True)
def skip_browsers(request: Any, browser_name: str) -> None:
    skip_browsers_names = _get_skiplist(
        request, ["chromium", "firefox", "webkit"], "browser"
    )

    if browser_name in skip_browsers_names:
        pytest.skip("skipped for this browser: {}".format(browser_name))


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def launch_arguments() -> Dict:
    return {}


@pytest.fixture(scope="session")
def context_arguments() -> Dict:
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
async def context(
    browser: Browser, context_arguments: Dict
) -> AsyncGenerator[BrowserContext, None]:
    context = await browser.newContext(**context_arguments)
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


@pytest.fixture(scope="session")
def is_webkit(browser_name: str) -> bool:
    return browser_name == "webkit"


@pytest.fixture(scope="session")
def is_firefox(browser_name: str) -> bool:
    return browser_name == "firefox"


@pytest.fixture(scope="session")
def is_chromium(browser_name: str) -> bool:
    return browser_name == "chromium"


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
