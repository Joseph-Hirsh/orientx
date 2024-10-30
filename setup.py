from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="orientx",
    version="0.1b2",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "orientx=orientx.main:main",
            "orientx-scrape=orientx.scraper.main:main",
            "orientx-parse=orientx.parser.main:main",
            "orientx-classify=orientx.classifier.main:main",
            "orientx-analyze=orientx.analyzer.main:main"
        ],
    },
)