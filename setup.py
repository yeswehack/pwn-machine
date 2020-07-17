#!/usr/bin/env python
import os
from setuptools import setup, find_packages

path = os.path.dirname(__file__)
long_description = open(os.path.join(path, "README.md"), "r", encoding="utf8").read()
version_file = os.path.join(path, "pwnmachine", "version.txt")
with open(version_file, "r") as f:
    version = f.read().strip()

setup(
    name="pwn-machine",
    version=version,
    packages=find_packages(),
    description="Simple self hosting solution based on docker for bug hunters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yeswehack/pwn-machine",
    author="@BitK_",
    author_email="bitk@yeswehack.com",
    install_requires=[
        "click==7.1.2",
        "dnspython==1.16.0",
        "docker==4.2.2",
        "docker-compose==1.26.2",
        "dockerpty==0.4.1",
        "docopt==0.6.2",
        "paramiko==2.7.1",
        "pyaml==20.4.0",
        "requests==2.24.0",
        "tqdm==4.47.0",
        "tabulate==0.8.7",
    ],
    package_data={"skel": ["*"]},
    include_package_data=True,
    entry_points={"console_scripts": ["pm=pwnmachine.cli:cli"]},
)
