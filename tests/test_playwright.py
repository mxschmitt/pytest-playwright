import pytest

@pytest.mark.asyncio
async def test_hello_default(page):
    await page.setContent('<span id="foo">bar</span>')
    assert await page.querySelector("#foo")