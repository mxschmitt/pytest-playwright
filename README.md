# Pytest Playwright Plugin (moved over to [microsoft/pytest-playwright](https://github.com/microsoft/playwright-pytest#readme))

![CI](https://github.com/mxschmitt/pytest-playwright/workflows/CI/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/pytest-playwright)](https://pypi.org/project/pytest-playwright/)
[![Coverage Status](https://coveralls.io/repos/github/mxschmitt/pytest-playwright/badge.svg?branch=master)](https://coveralls.io/github/mxschmitt/pytest-playwright?branch=master)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

> A Pytest wrapper for [Playwright](https://github.com/microsoft/playwright-python) to automate web browsers (Chromium, Firefox, WebKit).

## Features

- Have a separate new page and context for each test with Pytest fixtures
- Run your end-to-end tests on multiple browsers by a CLI argument
- Run them headful with the `--headful` argument to debug them easily
- Using [base-url](https://github.com/pytest-dev/pytest-base-url) to only use the relative URL in your `Page.goto` calls

## Installation

```
pip install pytest-playwright
```

Basic example for more see the [examples sections](#examples) as a reference.

```py
def test_is_chromium(page):
    page.goto("https://www.google.com")
    page.type("input[name=q]", "Playwright GitHub")
    page.click("input[type=submit]")
    page.waitForSelector("text=microsoft/Playwright")
```

## Fixtures

### `browser_name` - session scope

A string that contains the current browser name.

### `browser` - session scope

A Playwright browser instance for the whole test run.

### `context` - function scope

A separate Playwright context instance for each new test.

### `page` - function scope

A separate Playwright page instance for each new test.

### `launch_arguments` - session scope

A fixture that you can define to overwrite the launch arguments. It should return a Dict.

### `context_arguments` - session scope

A fixture that you can define to overwrite the context arguments. It should return a Dict.

### `is_chromium`, `is_firefox`, `is_webkit` - session scope

A fixture which is a boolean if a specific execution is made by the specified browser.

## CLI arguments

### `--browser`

By default, the tests run on the Chromium browser. You can pass multiple times the `--browser` flag to run it on different browsers or a single time to run it only on a specific browser.

Possible values: `chromium`, `firefox`, `webkit`

### `--headful`

By default, the tests run in headless mode. You can pass the `--headful` CLI flag to run the browser in headful mode.

## Examples

### Skipping by browser type

```py
import pytest

@pytest.mark.skip_browser("firefox")
def test_is_chromium(page):
    page.goto("https://www.google.com")
    # ...
```

### Running only on a specific browser

```py
import pytest

@pytest.mark.only_browser("chromium")
def test_is_chromium(page):
    page.goto("https://www.google.com")
    # ...
```

### Handle base-url

Start Pytest with the `base-url` argument. Example: `pytest --base-url http://localhost:8080`

```py
def test_is_chromium(page):
    page.goto("/admin")
    # -> Will result in http://localhost:8080/admin
```

### Using Mypy types for auto completion

```py
from playwright.sync_api import Page

def test_my_test(page: Page):
    page.goto("/admin")
    # ...
```
