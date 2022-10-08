import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
    with open("README.md", "r") as fh:
        long_description = fh.read()
else:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="binusmayapy",
    version="1.0.0",
    description="Python wrapper for Binusmaya web API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Raditya Harya",
    author_email="radityaharya02@gmail.com",
    url="https://github.com/radityaharya/binusmaya_py",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "requests",
        "selenium",
        "selenium_wire",
    ],
)
