# Pytest Playwright

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

## CLI arguments

### `--browser`

Per default, the tests run on all the browsers. You can pass multiple times the `--browser` flag to run it on different browsers or a single time to run it only on a specific browser.

Possible values: `chromium`, `firefox`, `webkit`

### `--headful`

Per default, the tests run in headless mode. You can pass the `--headful` CLI flag to run the browser in headful mode.
