from typing import Any


def test_simple(testdir: Any) -> None:
    """Make sure that our plugin works."""

    # create a temporary pytest test file
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.asyncio
        async def test_hello_default(page):
            await page.setContent('<span id="foo">bar</span>')
            assert await page.querySelector("#foo")
            print("done")
    """
    )

    # run all tests with pytest
    result = testdir.runpytest()

    result.assert_outcomes(passed=3)
