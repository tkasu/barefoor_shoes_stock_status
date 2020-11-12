#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Tomi Kasurinen",
    author_email="tomi.kasurinen@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Simple scraper so my wife can get the latest stock status of her favourite barefoot shoes",
    entry_points={
        "console_scripts": [
            "barefoor_shoes_stock_status=barefoor_shoes_stock_status.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="barefoor_shoes_stock_status",
    name="barefoor_shoes_stock_status",
    packages=find_packages(
        include=["barefoor_shoes_stock_status", "barefoor_shoes_stock_status.*"]
    ),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tkasu/barefoor_shoes_stock_status",
    version="0.1.0",
    zip_safe=False,
)
