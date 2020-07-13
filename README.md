# Pytest Playwright Plugin

![CI](https://github.com/mxschmitt/pytest-playwright/workflows/CI/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/pytest-playwright)](https://pypi.org/project/pytest-playwright/)
[![Coverage Status](https://coveralls.io/repos/github/mxschmitt/pytest-playwright/badge.svg?branch=master)](https://coveralls.io/github/mxschmitt/pytest-playwright?branch=master)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

> A Pytest wrapper for Playwright to automate web browsers (Chromium, Firefox, WebKit).

## Features

- Have a separate new page and context for each test with Pytest fixtures
- Run your end-to-end tests on multiple browsers by a CLI argument
- Run them headful with the `--headful` argument to debug them easily
- Using [base-url](https://github.com/pytest-dev/pytest-base-url) to only use the relative URL in your `Page.goto` calls

## Fixtures

### `browser_name` - session scope

A string which contains the current browser name.

### `browser` - session scope

A Playwright browser instance for the whole test run.

### `context` - function scope

A separate Playwright context instance for each new test.

### `page` - function scope

A separate Playwright page instance for each new test.

### `launch_arguments` - session scope

A fixture which you can define to overwrite the launch arguments. It should return a Dict.

### `context_arguments` - session scope

A fixture which you can define to overwrite the context arguments. It should return a Dict.

### `is_chromium`, `is_firefox`, `is_webkit` - session scope

A fixture which is a boolean if a specific execution is made by the specified browser.

## CLI arguments

### `--browser`

Per default, the tests run on all the browsers. You can pass multiple times the `--browser` flag to run it on different browsers or a single time to run it only on a specific browser.

Possible values: `chromium`, `firefox`, `webkit`

### `--headful`

Per default, the tests run in headless mode. You can pass the `--headful` CLI flag to run the browser in headful mode.
