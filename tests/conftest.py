import sys
import os

pytest_plugins = ["pytester"]

# The testdir fixture which we use to perform unit tests will set the home directory
# To a temporary directory of the created test. This would result that the browsers will
# be re-downloaded each time. By setting the pw browser path directory we can prevent that.
if sys.platform == "darwin":
    playwright_browser_path = os.path.expanduser("~/Library/Caches/ms-playwright")
elif sys.platform == "linux":
    playwright_browser_path = os.path.expanduser("~/.cache/ms-playwright")
else:
    raise ValueError("Not supported!")

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = playwright_browser_path
