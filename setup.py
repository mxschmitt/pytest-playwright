import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytest_playwright",
    version="0.0.1",
    author="Max Schmitt",
    author_email="max@schmitt.mx",
    description="A pytest wrapper with fixtures for Playwright to automate web browsers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mxschmitt/pytest-playwright",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["playwright","pytest", "pytest-base-url"],
    entry_points={"pytest11": ["playwright = pytest_playwright.pytest_playwright"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Pytest"
    ],
    python_requires=">=3.7",
)
