import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytest-playwright",
    author="Max Schmitt",
    author_email="max@schmitt.mx",
    description="A pytest wrapper with fixtures for Playwright to automate web browsers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mxschmitt/pytest-playwright",
    packages=["pytest_playwright"],
    include_package_data=True,
    install_requires=["playwright", "pytest", "pytest-base-url"],
    entry_points={"pytest11": ["playwright = pytest_playwright.pytest_playwright"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    python_requires=">=3.7",
    use_scm_version={
        "version_scheme": "post-release",
        "write_to": "pytest_playwright/_repo_version.py",
        "write_to_template": 'version = "{version}"\n',
    },
    setup_requires=["setuptools_scm"],
)
