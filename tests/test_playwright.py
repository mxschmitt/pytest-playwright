import pytest


def test_simple(testdir):
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
    print("really done")
    # check that all 4 tests passed
    result.assert_outcomes(passed=1)
