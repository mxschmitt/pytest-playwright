from typing import Any


def test_default(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_default(page):
            await page.setContent('<span id="foo">bar</span>')
            assert await page.querySelector("#foo")
            print("done")
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_multiple_browsers(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_multiple_browsers(page):
            await page.setContent('<span id="foo">bar</span>')
            assert await page.querySelector("#foo")
            print("done")
    """
    )
    result = testdir.runpytest(
        "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
    )
    result.assert_outcomes(passed=3)


def test_context_arguments(testdir: Any) -> None:
    testdir.makeconftest(
        """
        import pytest

        @pytest.fixture(scope="session")
        def context_arguments(request):
            return {"userAgent": "foobar"}
    """
    )
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_context_arguments(page):
            assert await page.evaluate("window.navigator.userAgent") == "foobar"
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_chromium(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_is_chromium(page, browser_name, is_chromium, is_firefox, is_webkit):
            assert browser_name == "chromium"
            assert is_chromium
            assert is_firefox is False
            assert is_webkit is False
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_firefox(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_is_firefox(page, browser_name, is_chromium, is_firefox, is_webkit):
            assert browser_name == "firefox"
            assert is_chromium is False
            assert is_firefox
            assert is_webkit is False
    """
    )
    result = testdir.runpytest("--browser", "firefox")
    result.assert_outcomes(passed=1)


def test_webkit(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_is_webkit(page, browser_name, is_chromium, is_firefox, is_webkit):
            assert browser_name == "webkit"
            assert is_chromium is False
            assert is_firefox is False
            assert is_webkit
    """
    )
    result = testdir.runpytest("--browser", "webkit")
    result.assert_outcomes(passed=1)


def test_goto(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_base_url(page, base_url):
            assert base_url == "https://example.com"
            await page.goto("/foobar")
            assert page.url == "https://example.com/foobar"
            await page.goto("https://www.google.com")
            assert page.url == "https://www.google.com/"
    """
    )
    result = testdir.runpytest("--base-url", "https://example.com")
    result.assert_outcomes(passed=1)


def test_skip_browsers(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        @pytest.mark.skip_browser("firefox")
        async def test_base_url(page, browser_name):
            assert browser_name in ["chromium", "webkit"]
    """
    )
    result = testdir.runpytest(
        "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
    )
    result.assert_outcomes(passed=2, skipped=1)


def test_only_browser(testdir: Any) -> None:
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        @pytest.mark.only_browser("firefox")
        async def test_base_url(page, browser_name):
            assert browser_name == "firefox"
    """
    )
    result = testdir.runpytest(
        "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
    )
    result.assert_outcomes(passed=1, skipped=2)
